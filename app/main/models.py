from django.contrib.auth.models import User
from django.db import models
import pytz
from django.utils.timezone import now


def get_moscow_time():
    moscow_tz = pytz.timezone("Europe/Moscow")
    return now().astimezone(moscow_tz)


# class Category_Access(models.Model):
#     name = models.CharField()
#
#     def __str__(self):
#         return f'id:{self.id}, name:{self.name}'


class Person(models.Model):
    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE)
    # access = models.ManyToManyField(Category_Access,related_name='person_access',verbose_name='Доступы')

    def __str__(self):
        return f'user_id:{self.user.id}, user_name:{self.user.name}'


class Site(models.Model):
    shablon_name = models.CharField(verbose_name='Имя Шаблона', default='1WIN')
    title = models.CharField(default="""
1WIN ВХОД НА ОФИЦИАЛЬНЫЙ САЙТ
    """, null=True, blank=True)
    description = models.TextField(verbose_name='Текст куска заголовка', default="""
<p> Используйте промокод: <a id="hero__promo" href="#">1winrupromo</a> и получите бонус <strong id="hero__price">до&nbsp;50&nbsp;000 рублей</strong> при регистрации.</p>
    """, null=True, blank=True)
    title_button = models.CharField(verbose_name='Текст заголовка кнопки', null=True, blank=True, default="""
Перейти на 1WIN
    """)
    link_for_site = models.CharField(verbose_name='Сслыка на заголовок продукта', null=True, blank=True)
    data_block = models.JSONField(verbose_name='Блоки', null=True, blank=True, default=[{
        'id': '',
        'title': 'О компании',
        'descr': '<p>Добро пожаловать на официальный сайт 1win casino. В 1 вин тебе повезет, даже если ты не новичок! И то, что ты попал на сайт 1win — твоя первая и главная победа! Врывайся в мир игровых слотов, и пусть удача сопутствует тебе. Игорные заведения — не только способ приятного времяпрепровождения, но и вероятность прилично поднять. Крути колесо и принимай удачу в гости! Счастливый билетик уже ждёт тебя на казино 1вин!</p>',
        'btn_text': 'Перейти на 1WIN',
        'btn_link': 'https://1wrefr.com/casino/list?open=register&sub1=clickid&sub2=dopid',
        'image': '',
    }])
    meta_teg = models.JSONField(verbose_name='Мета теги', null=True, blank=True, default=[{
        'id': '',
        'content': '',
    }])
    faq = models.JSONField(verbose_name='Вопросы Ответы', null=True, blank=True, default=[{
        'id': '1',
        'title': 'Вопрос',
        'description': 'Ответ'
    }])

    # Основная инфа
    domain_name = models.ForeignKey('Domain', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='site_domain')
    name_of_site = models.CharField(verbose_name='Название сайта', null=True, blank=True)
    main_link = models.CharField(null=True, blank=True, verbose_name='Основная ссылка на продукт казика')
    yandex_metrika = models.BigIntegerField(null=True, blank=True, verbose_name='Яндех Метрика')

    # Конфигурация сайта
    # id_vebmaster = models.ForeignKey(Vebmaster, on_delete=models.SET_NULL, related_name='site_id_vebmaster', null=True,
    #                                  blank=True)
    server = models.ForeignKey('Server', on_delete=models.SET_NULL, null=True, blank=True, related_name='site_server',
                               )
    promo_code = models.CharField(null=True, blank=True, verbose_name='Промо код')
    create_data = models.DateTimeField(default=get_moscow_time)
    update_data = models.DateTimeField(default=get_moscow_time)

    def __str__(self):
        return f'id:{self.id}, shablon_name:{self.shablon_name}'


class Server(models.Model):
    ip = models.CharField()
    status = models.CharField()
    user = models.CharField()
    password = models.CharField()
    skip = models.CharField(null=True, blank=True)
    Cf_email = models.CharField(null=True, blank=True)
    Cf_key = models.CharField(null=True, blank=True)
    Php_mode = models.CharField(null=True, blank=True)
    Registrar_vendor = models.CharField(null=True, blank=True)
    Registrar_username = models.CharField(null=True, blank=True)
    Registrar_apLKey = models.CharField(null=True, blank=True)
    create_data = models.DateTimeField(default=get_moscow_time)
    update_data = models.DateTimeField(default=get_moscow_time)

    def __str__(self):
        return f'id:{self.id}, ip:{self.ip}, status:{self.status}'


class Domain(models.Model):
    Username = models.CharField(null=True, blank=True)
    current_domain = models.CharField()
    domain_mask = models.CharField()
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True, blank=True, related_name='domain')
    status = models.CharField()
    redirect_domain = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='main_domain')
    yandex_metrika = models.BigIntegerField(null=True, blank=True, verbose_name='Яндех Метрика')
    vebmaster_id = models.CharField(null=True, blank=True, verbose_name='Вебмастер')
    create_data = models.DateTimeField(default=get_moscow_time)
    update_data = models.DateTimeField(default=get_moscow_time)

    def __str__(self):
        return f'id:{self.id}, current_domain:{self.current_domain}, status:{self.status}'
