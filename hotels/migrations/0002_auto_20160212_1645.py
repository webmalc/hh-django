# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-12 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='default',
        ),
        migrations.AddField(
            model_name='tariff',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='Is default?'),
        ),
        migrations.AddField(
            model_name='tariff',
            name='minimal_commission',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
