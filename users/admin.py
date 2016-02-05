from django.contrib.auth.admin import admin, UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress
from users.models import Profile, Organization, PartnershipOrder


class OrganizationAdmin(admin.ModelAdmin):
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


class PartnershipOrderAdmin(admin.ModelAdmin):
    """
    PartnershipOrder admin interface
    """
    list_display = ('get_full_name', 'created_at', 'created_by', 'status')
    list_display_links = ('get_full_name',)
    search_fields = ('last_name',)
    list_filter = ('created_at', )
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


class MyUserAdmin(UserAdmin):
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
