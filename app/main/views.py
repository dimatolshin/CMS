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
from datetime import timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv
import shutil

from .Serializers import request_body, response_serializer
from .models import *
from .services import *
from mysite import settings

load_dotenv()


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=timedelta(days=1),
            domain='gang-soft.com',
            httponly=False,
            secure=True,  # Только для HTTPS
            samesite='Strict',  # Защита от CSRF
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=timedelta(days=10),
            domain='gang-soft.com',
            httponly=False,
            secure=True,  # Только для HTTPS
            samesite='Strict',  # Защита от CSRF
        )

        response.data = {'access_token': access_token,
                         'refresh_token': refresh_token}
        return response


@swagger_auto_schema(
    methods=(['GET']),
    responses={
        '200': get_response_examples({'Info': 'Good'}),
    },
    tags=['TEST'],
)
@api_view(["GET"])
@site_authenticated
async def test_point(request):
    return JsonResponse({'Info': 'Good'}, status=200)


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
    domain_id = request.data.get('domain_id')

    if not domain_id:
        site = await Site.objects.filter(shablon_name=shablon_name).select_related('domain_name',
                                                                                   'server').afirst()
    if domain_id:
        site = await Site.objects.filter(domain_name__id=domain_id).select_related('domain_name',
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

    if not site :
        return JsonResponse({'Error': 'Site Unexist'}, status=404)

    update_fields = {}

    fields = [
        'title', 'description', 'title_button', 'link_for_site', 'data_block', 'meta_teg', 'faq', 'domain_name',
        'server',
        'name_of_site', 'main_link',
        'yandex_metrika',
        'promo_code'
    ]

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

    site = await Site.objects.filter(shablon_name=shablon_name).select_related('domain_name',
                                                                               'server').afirst()

    domain = await Domain.objects.filter(current_domain=site.domain_name.current_domain).select_related(
        'server').afirst()
    domain.server = site.server
    domain.status = 'Активен'

    domain.server.status = 'Активен'
    domain.Username = site.name_of_site
    await domain.asave()

    html_content = await sync_to_async(render_to_string)(f'{shablon_name}.html', {'site': site})

    os.makedirs(f'{shablon_name}', exist_ok=True)

    with open(f'{shablon_name}/index.html', 'w') as f:
        f.write(html_content)

    target_dir = f'static_sites/{domain.current_domain}'

    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Копируем все файлы из шаблона в целевую папку
    for root, dirs, files in os.walk(f'{shablon_name}'):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, start=f'{shablon_name}')
            dst_path = os.path.join(target_dir, rel_path)

            # Создаем подпапки, если их нет
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)

    base_url = "https://api.dynadot.com/api3.xml"
    params = {
        'key': os.getenv('DYNADOT_API_KEY'),
        'command': 'set_dns2',
        'domain': domain.current_domain,
        'main_record_type0': 'a',
        'main_record0': domain.server.ip,
        'subdomain0': 'www',
        'sub_record_type0': 'a',
        'sub_record0': domain.server.ip
    }

    response = requests.get(
        base_url,
        params=params,
        headers={'User-Agent': 'YourApp/1.0'}
    )

    return JsonResponse({'Info': 'Success',
                         'status_code': response.text}, status=200)


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
    current_domain_2 = request.data.get('current_domain_2')
    domain_mask_2 = request.data.get('domain_mask_2')
    status_2 = request.data.get('status_2')

    if not current_domain or not domain_mask or not status:
        return JsonResponse({'Error': 'Data uncorrect'}, status=404)

    domain = await Domain.objects.filter(current_domain=current_domain).select_related('server').afirst()

    if domain:
       domain.status=status
       await domain.asave()
    else:
        await Domain.objects.acreate(Username=domain_mask, current_domain=current_domain, domain_mask=domain_mask,
                                     status=status)


    if current_domain_2 and domain_mask_2 and status_2:
        await Domain.objects.acreate(Username=domain_mask_2, current_domain=current_domain_2, domain_mask=domain_mask_2,
                                     status=status_2)

        html_content = await sync_to_async(render_to_string)(f'redirect.html', {'current_domain_2': current_domain_2})

        os.makedirs(f'redirect_holder', exist_ok=True)

        with open(f'redirect_holder/index.html', 'w') as f:
            f.write(html_content)


        source_dir = f'static_sites/{domain.current_domain}'

        target_dir = f'static_sites/{current_domain_2}'

        # Если исходная папка существует
        if os.path.exists(source_dir):
            # Создаём целевую папку (если её нет)
            Path(target_dir).mkdir(parents=True, exist_ok=True)

            # Копируем ВСЁ содержимое из source_dir в target_dir
            for item in os.listdir(source_dir):
                src_path = os.path.join(source_dir, item)
                dst_path = os.path.join(target_dir, item)

                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
        else:
            print(f"Source directory {source_dir} does not exist!")

        Path(source_dir).mkdir(parents=True, exist_ok=True)

        for root, dirs, files in os.walk(f'redirect_holder'):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, start=f'redirect_holder')
                dst_path = os.path.join(source_dir, rel_path)

                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

            else:
                # Обычное копирование для остальных файлов
                shutil.copy2(src_path, dst_path)

        base_url = "https://api.dynadot.com/api3.xml"
        params = {
            'key': os.getenv('DYNADOT_API_KEY'),
            'command': 'set_dns2',
            'domain': current_domain_2,
            'main_record_type0': 'a',
            'main_record0': domain.server.ip,
            'subdomain0': 'www',
            'sub_record_type0': 'a',
            'sub_record0': domain.server.ip
        }

        requests.get(
            base_url,
            params=params,
            headers={'User-Agent': 'YourApp/1.0'}
        )


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
    all_domain = [await domains(item) async for item in Domain.objects.select_related('server').order_by('id').all()]

    count_domain = len(all_domain)
    paginator = Paginator(all_domain, 6)
    page_number = request.GET.get("page", 1)
    paginated_all_domain = paginator.get_page(page_number)

    data = {
        "all_domain": list(paginated_all_domain.object_list),
        "pages": math.ceil(count_domain / 6)
    }

    return JsonResponse(data, safe=False, status=200)


@swagger_auto_schema(
    methods=['GET'],
    responses={
        '404': get_response_examples({'error': True, 'Info': 'User unexist'}),
        '200': get_response_examples(schema=response_serializer.ServerSerializer)
    },
    tags=['Server'],
    operation_summary='ALl server list',
)
@api_view(["GET"])
@site_authenticated
async def get_all_server(request: HttpRequest):
    servers = [await all_servers(item) async for item in Server.objects.order_by('id').all()]

    count_page = len(servers)
    paginator = Paginator(servers, 6)
    page_number = request.GET.get("page", 1)
    paginated_all_server = paginator.get_page(page_number)

    data = {
        "all_domain": list(paginated_all_server.object_list),
        "pages": math.ceil(count_page / 6)
    }

    return JsonResponse(data, safe=False, status=200)
