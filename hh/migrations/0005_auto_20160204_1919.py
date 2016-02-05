# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hh', '0004_auto_20160204_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['-sorting', 'name'], 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterField(
            model_name='city',
            name='is_enabled',
            field=models.BooleanField(default=False, verbose_name='Is enabled?'),
        ),
    ]
