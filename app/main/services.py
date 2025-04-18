from drf_yasg import openapi
from rest_framework.serializers import Serializer
from functools import wraps
from django.http import JsonResponse
import requests
import os
from dotenv import load_dotenv
load_dotenv()

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
    }


async def custom_server(item):
    return {
        'id': item.id,
        'value': item.ip,
        'content': item.ip,
    }


async def data_blocklist(item):
    return {
        'id': item.get('id'),
        'title': item.get('title'),
        'descr': item.get('descr'),
        'btn_text': item.get('btn_text'),
        'btn_link': item.get('btn_link'),
        'image': item.get('image'),
    }


async def meta_teg_list(item):
    return {
        'id': item.get('id'),
        'name': item.get('name'),
        'content': item.get('content'),
    }


async def serverdata(site):
    return {
        "id": site.id if site else None,
        "domain_name": [await custom_domain_name(item) async for item in Domain.objects.all()],
        "server": [await custom_server(item) async for item in Server.objects.all()],
        "shablon_name": site.shablon_name if site else None,
        "title": site.title if site else None,
        "description": site.description if site else None,
        "title_button": site.title_button if site else None,
        "link_for_site": site.link_for_site if site else None,
        "data_block": [await data_blocklist(item) for item in site.data_block],
        "meta_teg": [await meta_teg_list(item) for item in site.meta_teg],
        "name_of_site": site.name_of_site if site else None,
        "main_link": site.main_link if site else None,
        "yandex_metrika": site.yandex_metrika if site else None,
        "promo_code": site.promo_code if site else None,
        "create_data": site.create_data if site else None,
    }


async def domains(item):
    return {
        'id': item.id if item.id else None,
        'Username': item.Username if item.Username else None,
        'Current_domain': item.current_domain if item.current_domain else None,
        'Domain_mask': item.domain_mask if item.domain_mask else None,
        'Server_id': item.server.id if item.server else None,
        'Status': item.status if item.status else None
    }


async def all_servers(item):
    return {
        'id': item.id if item.id else None,
        'ip': item.ip if item.ip else None,
        'status': item.status if item.status else None,
        'user': item.user if item.user else None,
        'password': item.password if item.password else None,
        'skip': item.skip if item.skip else None,
        'Cf_email': item.Cf_email if item.Cf_emailelse else None,
        'Cf_key': item.Cf_key if item.Cf_keyelse else None,
        'Php_mode': item.Php_mode if item.Php_mode else None,
        'Registrar_vendor': item.Registrar_vendor if item.Registrar_vendor else None,
        'Registrar_username': item.Registrar_username if item.Registrar_usernameelse else None,
        'Registrar_apLKey': item.Registrar_apLKey if item.Registrar_apLKey else None
    }


async def find_zone_id(domain_name):
    base_url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "X-Auth-Email": os.getenv('CLOUDFLARE_EMAIL'),
        "X-Auth-Key": os.getenv('CLOUDFLARE_API_KEY'),
        "Content-Type": "application/json"
    }

    params = {
        "name": f"{domain_name}",
    }

    response = requests.get(
        url=base_url,
        headers=headers,
        params=params
    )

    response.raise_for_status()  # Проверка на ошибки

    data = response.json()
    return data['result'][0]['id']


async def create_cloud_fire(zone_id,ip,domain_name,dop=''):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv('CLOUDFLARE_EMAIL'),
        'X-Auth-Key': os.getenv('CLOUDFLARE_API_KEY')
    }
    data = {
        "comment": "Domain verification record",
        "content": f"{ip}",
        "name": f"{dop}{domain_name}",
        "proxied": True,
        "ttl": 300,
        "type": "A"
    }
    return requests.post(base_url, headers=headers, json=data)


async def check_cloud_fire(zone_id,ip,domain_name,dop=''):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv('CLOUDFLARE_EMAIL'),
        'X-Auth-Key': os.getenv('CLOUDFLARE_API_KEY')
    }
    params = {
        "name": f'{dop}{domain_name}'
    }
    response = requests.get(base_url, headers=headers, params=params)

    response.raise_for_status()  # Проверка на ошибки

    data = response.json()
    return data['result'][0]['id']

async def delete_cloud_fire(zone_id,ip,domain_name,dns_record,dop=''):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record}"

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv('CLOUDFLARE_EMAIL'),
        'X-Auth-Key': os.getenv('CLOUDFLARE_API_KEY')
    }
    requests.delete(base_url, headers=headers)