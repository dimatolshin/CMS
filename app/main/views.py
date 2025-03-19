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

from .Serializers import request_body, response_serializer
from .models import *
from .services import get_response_examples, site_authenticated


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        # Устанавливаем Refresh Token в HTTP-Only cookie
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

        # Возвращаем Access Token в теле ответа
        response.data = {'access_token': access_token,
                         'refresh_token': refresh_token}
        return response


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
                                                                               'photo_about_3', 'id_vebmaster').afirst()

    data = response_serializer.SiteSerializer(site).data


    return JsonResponse(data, safe=False, status=200)

@swagger_auto_schema(
    methods=(['POST']),
    request_body=request_body.ChangeSite,
    responses={
        '404': get_response_examples({'error': True, 'Error': 'Данные переданы некорректные.'}),
        '200': get_response_examples({'Info':'Success'}),
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
        'title_5', 'description_5', 'domain_name', 'name_of_site', 'main_link', 'yandex_metrika',
        'id_vebmaster', 'valuable_main_domain', 'promo_code'
    ]

    image_fields = {
        'photo_1': 'photo_1',
        'photo_about_2': 'photo_about_2',
        'photo_about_3': 'photo_about_3'
    }

    for field, image_field in image_fields.items():
        if field in data:
            image = await Image.objects.acreate(name=f'{shablon_name}_{field}', image=data[field])
            update_fields[image_field] = image

    for field in fields:
        if field in data:
            update_fields[field] = data[field]

    if update_fields:
        await Site.objects.filter(shablon_name=shablon_name).aupdate(**update_fields)

    site = await Site.objects.filter(shablon_name=shablon_name).select_related('photo_1', 'photo_about_2',
                                                                               'photo_about_3', 'id_vebmaster').afirst()
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


