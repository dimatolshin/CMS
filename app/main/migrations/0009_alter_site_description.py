# Generated by Django 5.1.5 on 2025-03-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_site_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(default='\n     <p> Используйте промокод: <a id="hero__promo" href="#">1winrupromo</a> и&nbsp;получите бонус <strong id="hero__price">до&nbsp;50&nbsp;000 рублей</strong> при регистрации.</p>\n    ', verbose_name='Текст куска заголовка'),
        ),
    ]
