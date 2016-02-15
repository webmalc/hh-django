# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0009_metrostation_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='metrostation',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='metrostation',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
        ),
    ]