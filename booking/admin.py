from django.contrib import admin
from reversion.admin import VersionAdmin


class OrderAdmin(VersionAdmin):
    """
    Orders admin interface
    """
    list_display = (
        'id', 'begin', 'end', 'places', 'get_fio',
        'citizenship', 'phone', 'total', 'commission', 'agent_commission',
        'is_agent_order', 'status', 'accepted_room', 'created_at'
    )
    list_display_links = ('id',)
    search_fields = ('last_name', 'id', 'phone')
    list_filter = ('begin', 'citizenship', 'status', 'is_agent_order', 'created_at')
    fieldsets = (
        (
            'General', {
                'fields': ('begin', 'end', 'places', 'status')
            }
        ),
    )


