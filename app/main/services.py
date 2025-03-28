from drf_yasg import openapi
from rest_framework.serializers import Serializer
from functools import wraps
from django.http import JsonResponse

from .models import *


def get_response_examples(
        example: dict = {},
        description: str = '',
        schema: Serializer | Serializer | None = None,
):
    if schema is None:
        return openapi.Response(
            description=description,
            examples={"application/json": {'error': False} | example},
        )

    return openapi.Response(
        description=description,
        schema=schema
    )


def site_authenticated(view_func):
    @wraps(view_func)
    async def _wrapped_view(request, *args, **kwargs):
        site_access = request.COOKIES.get("access_token")
        site_refresh = request.COOKIES.get("refresh_token")

        if not site_access or not site_refresh:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        if not site_access:
            return JsonResponse({"detail": "Need create Acces"}, status=401)

        return await view_func(request, *args, **kwargs)

    return _wrapped_view


async def custom_domain_name(item):
    return {
        'id': item.id,
        'value': item.current_domain,
        'content': item.current_domain,
        'disabled':False if item.status == 'Активен' else True
    }


async def custom_server(item):
    return {
        'id': item.id,
        'value': item.ip,
        'content': item.ip,
        'disabled': False if item.status == 'Активен' else True
    }


async def serverdata(site):
    return {
        "id": site.id,
        "photo_1": site.photo_1.image_url,
        "photo_about_2": site.photo_about_2.image_url,
        "photo_about_3": site.photo_about_3.image_url,
        "domain_name": [await custom_domain_name(item) async for item in Domain.objects.all()],
        "server": [await custom_server(item) async for item in Server.objects.all()],
        "shablon_name": site.shablon_name,
        "title": site.title,
        "description": site.description,
        "title_button": site.title_button,
        "link_for_site": site.link_for_site,
        "title_1": site.title_1,
        "description_1": site.description_1,
        "button_1": site.button_1,
        "link_for_site_1": site.link_for_site_1,
        "title_2": site.title_2,
        "description_2": site.description_2,
        "button_2": site.button_2,
        "link_for_site_2": site.link_for_site_2,
        "title_3": site.title_3,
        "description_3": site.description_3,
        "button_3": site.button_3,
        "link_for_site_3": site.link_for_site_3,
        "title_4": site.title_4,
        "description_4": site.description_4,
        "title_5": site.title_5,
        "description_5": site.description_5,
        "name_of_site": site.name_of_site,
        "main_link": site.main_link,
        "yandex_metrika": site.yandex_metrika,
        "promo_code": site.promo_code,
        "create_data": site.create_data,
    }


async def domains(item):
    return {
        'id':item.id,
        'Username':item.Username,
        'Current_domain':item.current_domain,
        'Domain_mask':item.domain_mask,
        'Server_id':item.server.id,
        'Status':item.status
    }

async def all_servers(item):
    return {
        'id':item.id,
        'ip':item.ip,
        'status':item.status,
        'user':item.user,
        'password':item.password,
        'skip':item.skip,
        'Cf_email':item.Cf_email,
        'Cf_key':item.Cf_key,
        'Php_mode':item.Php_mode,
        'Registrar_vendor':item.Registrar_vendor,
        'Registrar_username':item.Registrar_username,
        'Registrar_apLKey':item.Registrar_apLKey
    }