from django.contrib.auth.admin import admin
from django.contrib import messages
from reversion.admin import VersionAdmin
from hotels.models import Tariff, TariffElement, MetroStation, Property


class PropertyAdmin(VersionAdmin):
    """
    Tariff admin interface
    """
    list_display = ('name', 'city', 'get_metro_stations_as_string', 'tariff', 'sorting', 'created_at', 'created_by')
    list_display_links = ('name',)
    list_filter = ('tariff', 'metro_stations')
    search_fields = ('name', 'city__name', 'city__alternate_names', 'metro_stations__name')
    raw_id_fields = ['city', 'created_by']
    fieldsets = (
        ('General', {
            'fields': ('name', 'description',)
        }),
        ('Location', {
            'fields': ('city', 'address', 'metro_stations', 'position')
        }),
        ('Options', {
            'fields': ('tariff', 'sorting', 'created_by',)
        }),
    )


class MetroStationsAdmin(VersionAdmin):
    """
    Tariff admin interface
    """
    list_display = ('name', 'city', 'color', 'created_at', 'created_by')
    list_display_links = ('name',)
    search_fields = ('name', 'city__name', 'city__alternate_names')
    raw_id_fields = ['city']
    fieldsets = (
        ('General', {
            'fields': ('name', 'city',)
        }),
        ('Options', {
            'fields': ('color', 'position')
        }),
    )

    class Media:
        js = ('admin/js/metro_stations.js',)


class TariffElementsInline(admin.TabularInline):
    """
    Tariff elements admin interface
    """
    model = TariffElement


class TariffAdmin(VersionAdmin):
    """
    Tariff admin interface
    """
    list_display = ('name', 'is_default', 'minimal_commission', 'created_at', 'created_by')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('is_default',)
    actions = None
    fieldsets = (
        ('General', {
            'fields': ('name', 'minimal_commission',)
        }),
        ('Options', {
            'fields': ('is_default',)
        }),
    )
    inlines = [
        TariffElementsInline
    ]

    def delete_model(self, request, obj):
        if obj.is_default:
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, 'Cannot delete default tariff.')
        else:
            obj.delete()


admin.site.register(Tariff, TariffAdmin)
admin.site.register(Property,PropertyAdmin)
admin.site.register(MetroStation, MetroStationsAdmin)
