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
        'disabled':True if item.status=='Заблокирован' else False,
        'content': item.current_domain,
    }


async def custom_server(item):
    return {
        'id': item.id,
        'value': item.ip,
        'disabled': True if item.status == 'Заблокирован' else False,
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

async def faq(item):
    return {
        'id':item.get('id'),
        'title': item.get('title'),
        'description': item.get('description')
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
        "domain_name": site.domain_name.current_domain if site.domain_name else None,
        "server":[await custom_server(item) async for item in Server.objects.all()],
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
        "faq":[await faq(item) for item in site.faq],
        "promo_code": site.promo_code if site else None,
        "create_data": site.create_data if site else None,
    }

async def domains_redirect(item):
    return {
        'id': item.id if item.id else None,
        'Username': item.Username if item.Username else None,
        'Current_domain': item.current_domain if item.current_domain else None,
        'Domain_mask': item.domain_mask if item.domain_mask else None,
        'Server_id': item.server.id if item.server else None,
        'Status': item.status if item.status else None,
        'Yandex_Metrika': item.yandex_metrika if item.yandex_metrika else None,
        'Vebmaster_Id':item.vebmaster_id if item.vebmaster_id else None,
        'Create_Data': item.create_data if item.create_data else None,
        'update_data':item.update_data if item.update_data else None,

    }
from asgiref.sync import sync_to_async

async def domains(item):
    return {
        'id': item.id if item.id else None,
        'Username': item.Username if item.Username else None,
        'Current_domain': item.current_domain if item.current_domain else None,
        'Domain_mask': item.domain_mask if item.domain_mask else None,
        'Server_id': item.server.id if item.server else None,
        'Status': item.status if item.status else None,
        'Yandex_Metrika': item.yandex_metrika if item.yandex_metrika else None,
        'Vebmaster_Id': item.vebmaster_id if item.vebmaster_id else None,
        'Create_Data': item.create_data if item.create_data else None,
        'Update_Data': item.update_data if item.update_data else None,
        'Redirect_Domain':await domains_redirect(item.redirect_domain) if item.redirect_domain else None
    }


async def all_servers(item):
    return {
        'id': item.id if item.id else None,
        'ip': item.ip if item.ip else None,
        'status': item.status if item.status else None,
        'user': item.user if item.user else None,
        'password': item.password if item.password else None,
    }


async def find_zone_id(domain_name,name_server):
    base_url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "X-Auth-Email": os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
        "X-Auth-Key": os.getenv(f'CLOUDFLARE_API_KEY_{name_server}'),
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


async def create_cloud_fire(zone_id,ip,domain_name,name_server,dop=''):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
        'X-Auth-Key': os.getenv(f'CLOUDFLARE_API_KEY_{name_server}')
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

async def create_cloud_fire_txt(zone_id,domain_name,yandex_metrika,name_server):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
        'X-Auth-Key': os.getenv(f'CLOUDFLARE_API_KEY_{name_server}')
    }
    data = {
        "comment": "Domain verification record",
        "content": f'"yandex-verification: {yandex_metrika}"',
        "name": f"{domain_name}",
        "proxied": False,
        "ttl": 300,
        "type": "TXT"
    }
    return requests.post(base_url, headers=headers, json=data)


async def setting_full(zone_id,name_server):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl"
    headers = {
        "X-Auth-Email": os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
        "X-Auth-Key": os.getenv(f'CLOUDFLARE_API_KEY_{name_server}'),
        "Content-Type": "application/json"
    }

    params = {
        "value": "full"
    }

    response = requests.patch(
        url=base_url,
        headers=headers,
        json=params
    )

    response.raise_for_status()

async def check_cloud_fire(zone_id,ip,type,domain_name,name_server,dop=''):
    try:
        base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Email': os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
            'X-Auth-Key': os.getenv(f'CLOUDFLARE_API_KEY_{name_server}')
        }
        params = {
            "name": f'{dop}{domain_name}',
            "type":f'{type}',
        }
        response = requests.get(base_url, headers=headers, params=params)

        response.raise_for_status()  # Проверка на ошибки

        data = response.json()
        return data['result'][0]['id']
    except Exception:
        return False

async def delete_cloud_fire(zone_id,ip,domain_name,dns_record,name_server,dop=''):
    base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record}"

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': os.getenv(f'CLOUDFLARE_EMAIL_{name_server}'),
        'X-Auth-Key': os.getenv(f'CLOUDFLARE_API_KEY_{name_server}')
    }
    requests.delete(base_url, headers=headers)