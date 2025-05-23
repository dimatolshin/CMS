# Generated by Django 5.1.5 on 2025-05-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_site_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='access',
            field=models.ManyToManyField(related_name='person_access', to='main.categoryaccess', verbose_name='Доступы'),
        ),
    ]
