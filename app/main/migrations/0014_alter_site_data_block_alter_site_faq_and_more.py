# Generated by Django 5.1.5 on 2025-04-02 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_site_title_button'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='data_block',
            field=models.JSONField(blank=True, default=[{'btn_link': 'https://1wrefr.com/casino/list?open=register&sub1=clickid&sub2=dopid', 'btn_text': 'Перейти на 1WIN', 'descr': '<p>Добро пожаловать на официальный сайт 1win casino. В 1 вин тебе повезет, даже если ты не новичок! И то, что ты попал на сайт 1win — твоя первая и главная победа! Врывайся в мир игровых слотов, и пусть удача сопутствует тебе. Игорные заведения — не только способ приятного времяпрепровождения, но и вероятность прилично поднять. Крути колесо и принимай удачу в гости! Счастливый билетик уже ждёт тебя на казино 1вин!</p>', 'id': '', 'image': '', 'title': 'О компании'}], null=True, verbose_name='Блоки'),
        ),
        migrations.AlterField(
            model_name='site',
            name='faq',
            field=models.JSONField(blank=True, default=[{'description': 'Ответ', 'id': '', 'title': 'Вопрос'}], null=True, verbose_name='Вопросы Ответы'),
        ),
        migrations.AlterField(
            model_name='site',
            name='meta_teg',
            field=models.JSONField(blank=True, default=[{'content': '', 'id': '', 'name': ''}], null=True, verbose_name='Мета теги'),
        ),
    ]
