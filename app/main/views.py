from rest_framework_simplejwt.views import TokenObtainPairView
from django.template.loader import render_to_string
from drf_yasg.utils import swagger_auto_schema
from adrf.decorators import api_view
from django.http import HttpRequest, JsonResponse

from django.core.paginator import Paginator
import math
from datetime import timedelta, date
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

import shutil
import json

from .Serializers import request_body, response_serializer
from .models import *
from .services import *
from mysite import settings

load_dotenv()


def get_moscow_time():
    moscow_tz = pytz.timezone("Europe/Moscow")
    return now().astimezone(moscow_tz)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=timedelta(days=1),
            # domain='gang-soft.com',
            httponly=False,
            secure=False,  # Только для HTTPS
            samesite='Strict',  # Защита от CSRF
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=timedelta(days=10),
            #             domain='gang-soft.com',
            httponly=False,
            secure=False,  # Только для HTTPS
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
    current_domain = request.data.get('current_domain')

    if not current_domain:
        site = await Site.objects.filter(shablon_name=shablon_name.upper()).select_related('domain_name',
                                                                                           'server').afirst()
    if current_domain:
        site = await Site.objects.filter(shablon_name=current_domain).select_related('domain_name',
                                                                                     'server').afirst()
        if not site:
            site = await Site.objects.filter(shablon_name=shablon_name.upper()).select_related('domain_name',
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
            domain = await  Domain.objects.filter(current_domain=data['domain_name'].strip()).afirst()
            if domain:
                update_fields['domain_name'] = domain
        if field in data:
            update_fields[field] = data[field]

    if update_fields:
        site = await Site.objects.filter(shablon_name=update_fields['domain_name'].current_domain).select_related(
            'domain_name',
            'server').afirst()
        if site:
            await Site.objects.filter(shablon_name=update_fields['domain_name'].current_domain).aupdate(**update_fields)

        else:
            await Site.objects.acreate(**update_fields, shablon_name=update_fields['domain_name'].current_domain)

    site = await Site.objects.filter(shablon_name=update_fields['domain_name'].current_domain).select_related(
        'domain_name',
        'server').afirst()

    faq = {

        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item['title'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item['description']
                }
            } for item in site.faq
        ]
    }
    script = f"<script type='application/ld+json'>{json.dumps(faq, ensure_ascii=False, separators=(',', ':'))}</script>"

    domain = await Domain.objects.filter(current_domain=site.domain_name.current_domain).select_related(
        'server').afirst()
    domain.server = site.server
    domain.status = 'Активен'
    domain.yandex_metrika = site.yandex_metrika

    domain.Username = site.name_of_site
    domain.update_data = get_moscow_time()
    await domain.asave()

    target_dir = f'static_sites/{domain.current_domain}/media'

    Path(target_dir).mkdir(parents=True, exist_ok=True)

    for item in site.data_block:
        if not item['image']:
            continue

            # Извлекаем Base64 (удаляем префикс data:image/... если есть)
        base64_data = item['image'].split(",")[1] if "," in item['image'] else item['image']

        try:
            # Декодируем Base64 в бинарные данные
            image_data = base64.b64decode(base64_data)

            # Открываем изображение с помощью Pillow
            img = Image.open(BytesIO(image_data))

            # Сохраняем в WebP (можно регулировать качество `quality=90`)
            output_path = Path(target_dir) / f"{item['id']}.webp"
            img.save(output_path, "WEBP", quality=90)  # quality от 1 до 100

        except Exception as e:
            return JsonResponse(
                {"error": f"Ошибка при сохранении изображения {item['id']}: {e}"},
                status=400
            )

    html_content = await sync_to_async(render_to_string)(f'{shablon_name}.html', {'site': site, 'script': script})

    os.makedirs(f'{shablon_name}', exist_ok=True)

    with open(f'{shablon_name}/index.html', 'w') as f:
        f.write(html_content)

    with open(f'{shablon_name}/robots.txt', 'w') as f:
        f.write(f"""User-agent: *
Sitemap: https://{domain.current_domain}/sitemap.xml""")

    with open(f'{shablon_name}/sitemap.xml', 'w') as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> 
    <url>
        <loc>https://{domain.current_domain}/</loc>
        <lastmod>{date.today()}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
    """)

    target_dir = f'static_sites/{domain.current_domain}'
    # Копируем все файлы из шаблона в целевую папку
    for root, dirs, files in os.walk(f'{shablon_name}'):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, start=f'{shablon_name}')
            dst_path = os.path.join(target_dir, rel_path)

            # Создаем подпапки, если их нет
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)

    zone_id = await find_zone_id(domain_name=domain.current_domain, name_server=shablon_name)
    await setting_full(zone_id, name_server=shablon_name)
    dns_record = await check_cloud_fire(zone_id=zone_id, type='A', ip=domain.server.ip,
                                        domain_name=domain.current_domain, name_server=shablon_name)

    if dns_record:
        await delete_cloud_fire(zone_id=zone_id, ip=domain.server.ip, domain_name=domain.current_domain,
                                dns_record=dns_record, name_server=shablon_name)

    await create_cloud_fire(zone_id=zone_id, ip=domain.server.ip, domain_name=domain.current_domain,
                            name_server=shablon_name)

    dns_record_1 = await check_cloud_fire(zone_id=zone_id, type='A', ip=domain.server.ip,
                                          domain_name=domain.current_domain, name_server=shablon_name,
                                          dop='www.')
    if dns_record_1:
        await delete_cloud_fire(zone_id=zone_id, ip=domain.server.ip, domain_name=domain.current_domain,
                                dns_record=dns_record_1, name_server=shablon_name, dop='www.')
    await create_cloud_fire(zone_id=zone_id, ip=domain.server.ip, domain_name=domain.current_domain,
                            name_server=shablon_name, dop='www.')

    dns_record_2 = await check_cloud_fire(zone_id=zone_id, ip=domain.server.ip, type='TXT', name_server=shablon_name,
                                          domain_name=domain.current_domain)
    if dns_record_2:
        await delete_cloud_fire(zone_id=zone_id, ip=domain.server.ip, domain_name=domain.current_domain,
                                dns_record=dns_record_2, name_server=shablon_name)
    await create_cloud_fire_txt(zone_id=zone_id, domain_name=domain.current_domain, yandex_metrika=site.yandex_metrika,
                                name_server=shablon_name)

    return JsonResponse({'Info': 'Success'}, status=200)


@swagger_auto_schema(
    methods=(['POST']),
    request_body=request_body.GetDomainData,
    responses={
        '404': get_response_examples({'error': True, 'Error': 'Данные переданы некорректные.'}),
        '200': get_response_examples({'Info': 'Success'}),
    },
    tags=['Боты'],
    operation_summary='получение инфы от ботов ')
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
        domain.status = status
        domain.update_data = get_moscow_time()
        site = await Site.objects.filter(shablon_name=current_domain).select_related('domain_name',
                                                                                     'server').afirst()
        await domain.asave()
    if not domain:
        await Domain.objects.acreate(Username=domain_mask, current_domain=current_domain, domain_mask=domain_mask,
                                     status=status)

    if current_domain_2 and domain_mask_2 and status_2:

        await Domain.objects.acreate(Username=domain_mask_2, current_domain=current_domain_2, domain_mask=domain_mask_2,
                                     status=status_2, redirect_domain=domain, server=domain.server)

        domain2 = await Domain.objects.filter(current_domain=current_domain_2).select_related('server').afirst()
        domain.redirect_domain = domain2
        await domain.asave()
        if site:
            await Site.objects.acreate(shablon_name=current_domain_2, title=site.title, description=site.description,
                                       title_button=site.title_button, link_for_site=site.link_for_site,
                                       data_block=site.data_block, meta_teg=site.meta_teg, faq=site.faq,
                                       domain_name=domain2, name_of_site=site.name_of_site, main_link=site.main_link,
                                       yandex_metrika=site.yandex_metrika, promo_code=site.promo_code,
                                       server=site.server)
        html_content = await sync_to_async(render_to_string)(f'redirect.html', {'current_domain_2': current_domain_2})

        os.makedirs(f'redirect_holder', exist_ok=True)

        with open(f'redirect_holder/index.html', 'w') as f:
            f.write(html_content)

            with open(f'static_sites/{current_domain}/robots.txt', 'w') as f:
                f.write(f"""User-agent: *
Sitemap: https://{current_domain_2}/sitemap.xml""")

            with open(f'static_sites/{current_domain}/sitemap.xml', 'w') as f:
                f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> 
    <url>
        <loc>https://{current_domain_2}/index.html</loc>
        <lastmod>{date.today()}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
    """)

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

        zone_id = await find_zone_id(domain_name=domain2.current_domain, name_server=domain_mask_2.upper())
        await setting_full(zone_id, name_server=domain_mask_2.upper())
        dns_record = await check_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, type='A',
                                            name_server=domain_mask_2.upper(),
                                            domain_name=domain2.current_domain)
        if dns_record:
            await delete_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, domain_name=domain2.current_domain,
                                    name_server=domain_mask_2.upper(),
                                    dns_record=dns_record)
        await create_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, domain_name=domain2.current_domain,
                                name_server=domain_mask_2.upper())

        dns_record_1 = await check_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, type='A',
                                              name_server=domain_mask_2.upper(),
                                              domain_name=domain2.current_domain, dop='www.')
        if dns_record_1:
            await delete_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, domain_name=domain2.current_domain,
                                    name_server=domain_mask_2.upper(),
                                    dns_record=dns_record_1, dop='www.')
        await create_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, domain_name=domain2.current_domain,
                                name_server=domain_mask_2.upper(), dop='www.')

        dns_record_2 = await check_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, type='TXT',
                                              name_server=domain_mask_2.upper(),
                                              domain_name=domain2.current_domain)
        if dns_record_2:
            await delete_cloud_fire(zone_id=zone_id, ip=domain2.server.ip, domain_name=domain2.current_domain,
                                    name_server=domain_mask_2.upper(),
                                    dns_record=dns_record_2)

        yandex_metrika = (
            await domain2.site_domain.afirst()).yandex_metrika if await domain2.site_domain.aexists() else None

        await create_cloud_fire_txt(zone_id=zone_id, domain_name=domain2.current_domain,
                                    yandex_metrika=yandex_metrika, name_server=domain_mask_2.upper())

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
    text = request.GET.get("text")
    filter_way = request.GET.get("filter_way")
    order_by_map = {
        "all_domain": "all",
        "active_domain": "Активен",
        "not_active_domain": "Не Активен",
        "block_domain": "Заблокирован",
    }

    order_by = order_by_map.get(filter_way)
    if not order_by:
        return JsonResponse({"error": "Invalid filter_way"}, status=400)

    if order_by == 'all':
        if text:
            query = [item async for item in
                     Domain.objects.filter(current_domain__icontains=text).select_related('server',
                                                                                          'redirect_domain__server').order_by(
                         'id').all()]

            count = len(query)
        else:
            query = [item async for item in
                     Domain.objects.select_related('server',
                                                   'redirect_domain__server').order_by(
                         'id').all()]
            count = len(query)
    else:

        if text:
            query = [item async for item in
                     Domain.objects.filter(current_domain__icontains=text, status=order_by).select_related('server',
                                                                                                           'redirect_domain__server').order_by(
                         'id').all()]
            count = len(query)
        else:
            query = [item async for item in
                     Domain.objects.filter(status=order_by).select_related('server',
                                                                           'redirect_domain__server').order_by(
                         'id').all()]
            count = len(query)

    all_domain = [await domains(item) for item in query]

    count_domain = len(all_domain)
    per_page = request.GET.get("per_page", 6)
    paginator = Paginator(all_domain, per_page)
    page_number = request.GET.get("page", 1)
    paginated_all_domain = paginator.get_page(page_number)

    count_all_domain = len([item async for item in
                            Domain.objects.select_related('server',
                                                          'redirect_domain__server').order_by(
                                'id').all()])

    count_active_domain = len([item async for item in
                               Domain.objects.filter(status='Активен').select_related('server',
                                                                                      'redirect_domain__server').order_by(
                                   'id').all()])

    count_not_active_domain = len([item async for item in
                                   Domain.objects.filter(status='Не Активен').select_related('server',
                                                                                             'redirect_domain__server').order_by(
                                       'id').all()])

    count_block_domain = len([item async for item in
                              Domain.objects.filter(status='Заблокирован').select_related('server',
                                                                                          'redirect_domain__server').order_by(
                                  'id').all()])

    data = {
        "all_domain": list(paginated_all_domain.object_list),
        "pages": math.ceil(count_domain / 6),
        "count_all_domain": count_all_domain,
        "count_concrete_domain": count,
        "count_active_domain": count_active_domain,
        "count_not_active_domain": count_not_active_domain,
        "count_block_domain": count_block_domain

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
    per_page = request.GET.get("per_page", 6)
    paginator = Paginator(servers, per_page)
    page_number = request.GET.get("page", 1)
    paginated_all_server = paginator.get_page(page_number)

    data = {
        "all_domain": list(paginated_all_server.object_list),
        "pages": math.ceil(count_page / 6)
    }

    return JsonResponse(data, safe=False, status=200)
