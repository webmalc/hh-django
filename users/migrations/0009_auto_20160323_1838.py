# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-23 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_usermessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='type',
            field=models.TextField(choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('danger', 'danger')], default='info', max_length=20),
        ),
    ]