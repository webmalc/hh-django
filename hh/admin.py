from django.contrib.auth.admin import admin
from django.db import models
from django import forms
from sitetree.admin import TreeItemAdmin, override_item_admin
from cities_light.admin import CityAdmin
from hh.models import City
from django.utils.translation import ugettext_lazy as _


class HHCityAdmin(CityAdmin):
    list_display = (
        'name', 'region', 'country', 'sorting', 'is_enabled',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class CustomTreeItemAdmin(TreeItemAdmin):
    fieldsets = (
        (_('Basic settings'), {
            'fields': ('parent', 'title', 'url',)
        }),
        (_('Access settings'), {
            'classes': ('collapse',),
            'fields': ('access_loggedin', 'access_guest', 'access_restricted', 'access_permissions', 'access_perm_type')
        }),
        (_('Display settings'), {
            'classes': ('collapse',),
            'fields': ('hidden', 'inmenu', 'inbreadcrumbs', 'insitetree')
        }),
        (_('Additional settings'), {
            'classes': ('collapse',),
            'fields': ('hint', 'description', 'alias', 'icon', 'urlaspattern')
        }),
    )

override_item_admin(CustomTreeItemAdmin)
admin.site.unregister(City)
admin.site.register(City, HHCityAdmin)
