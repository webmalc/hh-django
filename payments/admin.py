from django.contrib.auth.admin import admin
from reversion.admin import VersionAdmin
from payments.models import Payment


class PaymentAdmin(VersionAdmin):
    """
    Payments admin
    """
    model = Payment
    list_display = ('id', 'total', 'is_completed', 'user', 'order', 'comment', 'created_at')
    list_display_links = ('id', 'total')
    search_fields = ('id', 'user__username', 'user__last_name', 'order__id')
    list_filter = ('is_completed',)
    fields = (
        'total', 'is_completed', 'user', 'order', 'comment',
        'created_by', 'created_at', 'modified_at', 'modified_by'
    )

    raw_id_fields = ['user', 'order']
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at')
    ordering = ('-created_at',)

    class Media:
        css = {
            'all': ('admin/css/payments.css',)
        }
        js = ('admin/js/payments.js',)

admin.site.register(Payment, PaymentAdmin)

