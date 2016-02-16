# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160212_1637'),
        ('hotels', '0013_auto_20160215_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('calculation_type', models.CharField(choices=[('per_person', 'За человека'), ('per_room', 'За комнату')], default='per_person', max_length=20)),
                ('places', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(choices=[('per_person', 'За человека'), ('per_room', 'За комнату')], default='mixed', max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels_room_created_by', to='users.User')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels_room_modified_by', to='users.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['name', '-sorting'], 'permissions': (('can_search_property', 'Can search property'), ('can_book_property', 'Can book property'), ('can_send_property_orders', 'Can send orders to property')), 'verbose_name_plural': 'properties'},
        ),
        migrations.AddField(
            model_name='room',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.Property'),
        ),
    ]
