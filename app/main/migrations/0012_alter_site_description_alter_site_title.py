# Generated by Django 5.1.5 on 2025-04-02 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_site_photo_about_2_remove_site_photo_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='description',
            field=models.TextField(blank=True, default='\n<p> Используйте промокод: <a id="hero__promo" href="#">1winrupromo</a> и получите бонус <strong id="hero__price">до&nbsp;50&nbsp;000 рублей</strong> при регистрации.</p>\n    ', null=True, verbose_name='Текст куска заголовка'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title',
            field=models.CharField(blank=True, default='\n1WIN ВХОД НА ОФИЦИАЛЬНЫЙ САЙТ\n    ', null=True),
        ),
    ]
