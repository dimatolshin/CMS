from django.shortcuts import render
from psycopg2.extensions import JSONB
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from adrf.decorators import api_view
from django.http import HttpRequest, JsonResponse
import os
from asgiref.sync import sync_to_async
import zipfile
import base64
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
import math

from .Serializers import request_body, response_serializer
from .models import *
from .services import *


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,  # Только для HTTPS
            samesite='Strict',  # Защита от CSRF
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  # Только для HTTPS
            samesite='Strict',  # Защита от CSRF
        )

        response.data = {'access_token': access_token,
                         'refresh_token': refresh_token}
        return response


@api_view(["GET"])
@site_authenticated
async def test_point(request):
    return JsonResponse({'Info':'Good'},status=200)


@swagger_auto_schema(
    methods=(['POST']),
    request_body=request_body.ShablonName,
    responses={
        '404': get_response_examples({'error': True, 'Error': 'Данные переданы некорректные.'}),
        '200': get_response_examples(schema=response_serializer.SiteSerializer),
    },
    tags=['Генератор'],
    operation_summary='Получение инфы шаблона',

)
@api_view(["POST"])
@site_authenticated
async def get_shablon_data(request):
    shablon_name = request.data.get('shablon_name')

    if not shablon_name:
        return JsonResponse({'Error': 'Not shablon_name'}, status=404)
    site = await Site.objects.filter(shablon_name=shablon_name).select_related('photo_1', 'photo_about_2',
                                                                               'photo_about_3', 'domain_name',
                                                                               'server').afirst()

    data = await serverdata(site)

    return JsonResponse(data, safe=False, status=200)


@swagger_auto_schema(
    methods=(['POST']),
    request_body=request_body.ChangeSite,
    responses={
        '404': get_response_examples({'error': True, 'Error': 'Данные переданы некорректные.'}),
        '200': get_response_examples({'Info': 'Success'}),
    },
    tags=['Генератор'],
    operation_summary='Сохранения инфы шаблона',

)
@api_view(["POST"])
@site_authenticated
async def change_shablon_data(request):
    data = request.data

    shablon_name = data.get('shablon_name')
    site = await Site.objects.filter(shablon_name=shablon_name).afirst()

    if not site:
        return JsonResponse({'Error': 'Site Unexist'}, status=404)

    update_fields = {}

    fields = [
        'title', 'description', 'title_button', 'link_for_site', 'title_1', 'description_1',
        'button_1', 'link_for_site_1', 'title_2', 'description_2', 'button_2', 'link_for_site_2',
        'title_3', 'description_3', 'button_3', 'link_for_site_3', 'title_4', 'description_4',
        'title_5', 'description_5', 'domain_name', 'server', 'name_of_site', 'main_link', 'yandex_metrika',
        'promo_code'
    ]

    image_fields = {
        'photo_1': 'photo_1',
        'photo_about_2': 'photo_about_2',
        'photo_about_3': 'photo_about_3'
    }

    for field, image_field in image_fields.items():

        if field in data:
            image_data = data[field].split(';base64,')[1]

            decoded_image = base64.b64decode(image_data)

            image = Image(name=f'{shablon_name}_{field}')
            await sync_to_async(image.image.save)(f'{shablon_name}_{field}.webp', ContentFile(decoded_image),
                                                  save=False)
            await image.asave()
            update_fields[image_field] = image

    for field in fields:
        if 'server' in data and data['server']:
            server = await Server.objects.filter(ip=data['server']).afirst()
            if server:
                update_fields['server'] = server

        if 'domain_name' in data and data['domain_name']:
            domain = await  Domain.objects.filter(current_domain=data['domain_name']).afirst()
            if domain:
                update_fields['domain_name'] = domain
        if field in data:
            update_fields[field] = data[field]

    if update_fields:
        await Site.objects.filter(shablon_name=shablon_name).aupdate(**update_fields)

    site = await Site.objects.filter(shablon_name=shablon_name).select_related('photo_1', 'photo_about_2',
                                                                               'photo_about_3', 'domain_name',
                                                                               'server').afirst()

    domain = await Domain.objects.filter(current_domain=site.domain_name.current_domain).afirst()
    domain.server = site.server
    domain.Username = site.name_of_site
    await domain.asave()

    html_content = await sync_to_async(render_to_string)(f'{shablon_name}.html', {'site': site})

    os.makedirs(f'{shablon_name}', exist_ok=True)

    with open(f'{shablon_name}/{shablon_name}.html', 'w') as f:
        f.write(html_content)

    zip_file_path = f'{shablon_name}.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(f'{shablon_name}'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=f'{shablon_name}')
                zipf.write(file_path, arcname=arcname)

    return JsonResponse({'Info': 'Success'}, status=200)


@swagger_auto_schema(
    methods=(['POST']),
    request_body=request_body.GetDomainData,
    responses={
        '404': get_response_examples({'error': True, 'Error': 'Данные переданы некорректные.'}),
        '200': get_response_examples({'Info': 'Success'}),
    },
    tags=['Боты'],
    operation_summary='получение инфы от ботов ',

)
@api_view(["POST"])
async def take_bot_data(request):
    current_domain = request.data.get('current_domain')
    domain_mask = request.data.get('domain_mask')
    status = request.data.get('status')

    if not current_domain or not domain_mask or not status:
        return JsonResponse({'Error': 'Data uncorrect'}, status=404)

    await Domain.objects.acreate(current_domain=current_domain, domain_mask=domain_mask,
                                 status=status)

    return JsonResponse({'Info': 'Success'}, status=200)


@swagger_auto_schema(
    methods=['GET'],
    responses={
        '404': get_response_examples({'error': True, 'Info': 'User unexist'}),
    },
    tags=['Domain'],
    operation_summary='Получение all domain list',
)
@api_view(["GET"])
@site_authenticated
async def get_all_domain(request: HttpRequest):
    all_domain = [await domains(item) async for item in Domain.objects.select_related('server').all()]

    count_domain = len(all_domain)
    paginator = Paginator(all_domain, 6)
    page_number = request.GET.get("page", 1)
    paginated_all_domain = paginator.get_page(page_number)

    data = {
        "all_domain": list(paginated_all_domain.object_list),
        "pages": math.ceil(count_domain // 6)
    }

    return JsonResponse(data, safe=False, status=200)


@swagger_auto_schema(
    methods=['GET'],
    responses={
        '404': get_response_examples({'error': True, 'Info': 'User unexist'}),
        '200':get_response_examples(schema=response_serializer.ServerSerializer)
    },
    tags=['Server'],
    operation_summary='ALl server list',
)
@api_view(["GET"])
@site_authenticated
async def get_all_server(request: HttpRequest):
    servers= [await all_servers(item) async for item in Server.objects.all()]

    count_page = len(servers)
    paginator = Paginator(servers, 6)
    page_number = request.GET.get("page", 1)
    paginated_all_server = paginator.get_page(page_number)

    data = {
        "all_domain": list(paginated_all_server.object_list),
        "pages": math.ceil(count_page // 6)
    }

    return JsonResponse(data,safe=False, status=200)
