# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-10 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20160309_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='accepted_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_accepted_room', to='hotels.Room', verbose_name='room'),
        ),
    ]
