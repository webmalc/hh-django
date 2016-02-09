from django.contrib.auth.admin import admin, UserAdmin
from reversion.helpers import patch_admin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin
from allauth.account.models import EmailAddress
from users.models import Profile, Organization, PartnershipOrder


class OrganizationAdmin(VersionAdmin):
    """
    Organization admin interface
    """
    list_display = ('type', 'name', 'created_at', 'created_by')
    list_display_links = ('type', 'name')
    search_fields = ('name', 'type')
    list_filter = ('type', 'created_at')
    fieldsets = (
        ('General', {
            'fields': ('type', 'name')
        }),
    )


class OrganizationInline(admin.TabularInline):
    """
    User organization admin interface
    """
    model = Organization


class PartnershipOrderAdmin(VersionAdmin):
    """
    PartnershipOrder admin interface
    """
    list_display = ('id', 'get_full_name', 'type', 'created_at', 'created_by', 'status')
    list_display_links = ('id', 'get_full_name',)
    search_fields = ('id', 'last_name', 'city__name', 'city__alternate_names')
    list_filter = ('status', 'created_at', )
    raw_id_fields = ('city', 'organization')
    fieldsets = (
        ('General', {
            'fields': ('last_name', 'first_name', 'patronymic', 'type', 'status')
        }),
        ('Contacts', {
            'fields': ('phone', 'city', 'organization')
        }),
        ('Other', {
            'fields': ('experience', 'comment')
        })
    )

    def set_approved(self, request, queryset):
        for order in queryset:
            order.status = 'approved'
            order.save()
        self.message_user(request, 'Orders successfully marked as approved.')
    set_approved.short_description = "Mark selected orders as approved"

    def set_canceled(self, request, queryset):
        for order in queryset:
            order.status = 'canceled'
            order.save()
        self.message_user(request, 'Orders successfully marked as canceled.')
    set_canceled.short_description = "Mark selected orders as canceled"

    def set_in_work(self, request, queryset):
        queryset.update(status='in_work')
        self.message_user(request, 'Orders successfully marked as processing.')
    set_in_work.short_description = "Mark selected orders as processing"

    actions = [set_in_work, set_approved, set_canceled]

    class Media:
        css = {
            'all': ('admin/css/partnership_orders.css',)
        }
        js = ('admin/js/partnership_orders.js',)


class ProfileInline(admin.StackedInline):
    """
    Profile admin interface
    """
    model = Profile
    verbose_name_plural = 'Profile'
    raw_id_fields = ('city', 'organization')


class EmailsInline(admin.TabularInline):
    """
    User emails admin interface
    """
    model = EmailAddress


class MyUserAdmin(UserAdmin, VersionAdmin):
    """
    User admin interface
    """
    list_display = UserAdmin.list_display + ('last_login',)
    list_filter = UserAdmin.list_filter + ('last_login',)
    inlines = [
        ProfileInline, EmailsInline
    ]
    fieldsets = (
        ('General', {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/users.css',)
        }


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PartnershipOrder, PartnershipOrderAdmin)
patch_admin(Group)

