# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0014_auto_20160216_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='gender',
            field=models.CharField(choices=[('mixed', 'Смешанный'), ('male', 'Мужской'), ('female', 'Женский')], default='mixed', max_length=20),
        ),
    ]