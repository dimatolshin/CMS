# Generated by Django 5.1.5 on 2025-04-18 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_site_meta_teg'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='redirect_domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_domain', to='main.domain'),
        ),
    ]
