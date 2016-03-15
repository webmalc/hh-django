from django.contrib import admin
from django.conf import settings
from reversion.admin import VersionAdmin
from booking.models import Order


class RoomInline(admin.TabularInline):
    model = Order.rooms.through
    raw_id_fields = ('room', )
    verbose_name = "room"
    verbose_name_plural = "rooms"
    extra = 2
    max_num = settings.HH_BOOKING_MAX_ORDER_ROOMS


class OrderAdmin(VersionAdmin):
    """
    Orders admin interface
    """
    list_display = (
        'id', 'status', 'begin', 'end', 'places', 'get_fio',
        'citizenship', 'phone', 'total', 'commission',
        'get_commission_sum', 'agent_commission', 'get_agent_commission_sum',
        'is_agent_order', 'get_property', 'accepted_room', 'created_by', 'created_at'
    )
    list_display_links = ('id', 'status')
    search_fields = ('last_name', 'id', 'phone', 'email', 'created_by__username')
    list_filter = ('begin', 'citizenship', 'status', 'is_agent_order', 'created_at')
    fieldsets = (
        (
            'General', {
                'fields': ('begin', 'end', 'places', 'status', 'comment', 'created_by', 'created_at')
            },
        ),
        (
            'Client', {
                'fields': ('last_name', 'first_name', 'patronymic', 'citizenship', 'phone', 'email')
            },
        ),
        (
            'Finances', {
                'fields': (
                    'total', 'commission', 'get_commission_sum',
                    'agent_commission', 'get_agent_commission_sum', 'is_agent_order'
                )
            }
        ),
        (
            'Room', {
                'fields': ('get_property', 'accepted_room',)
            }
        ),
    )
    readonly_fields = ('created_by', 'get_agent_commission_sum', 'get_commission_sum', 'created_at', 'get_property')
    raw_id_fields = ('accepted_room',)
    inlines = [
        RoomInline,
    ]

    class Media:
        js = ('admin/js/orders.js',)


admin.site.register(Order, OrderAdmin)
