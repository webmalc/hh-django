from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import admin
from django.db import models
from django import forms
from reversion.admin import VersionAdmin
from reversion.helpers import patch_admin
from sitetree.admin import TreeItemAdmin, override_item_admin
from django.contrib.sites.models import Site
from cities_light.admin import CityAdmin
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from avatar.models import Avatar
from hh.models import City, Region, Country


class HHCityAdmin(CityAdmin, VersionAdmin):
    list_display = (
        'name', 'get_first_alternate_name', 'region', 'country', 'sorting', 'is_enabled',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

    def set_enabled(self, request, queryset):
        queryset.update(is_enabled=True)
    set_enabled.short_description = "Mark selected cities as enabled"

    def set_disabled(self, request, queryset):
        queryset.update(is_enabled=False)
    set_disabled.short_description = "Mark selected cities as disabled"

    actions = [set_enabled, set_disabled]


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
patch_admin(Region)
patch_admin(Country)
patch_admin(EmailAddress)
patch_admin(SocialAccount)
patch_admin(SocialApp)
patch_admin(SocialToken)
patch_admin(Avatar)
patch_admin(Site)
