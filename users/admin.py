from django.contrib.auth.admin import admin, UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress
from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'
    raw_id_fields = ("city",)


class EmailsInline(admin.TabularInline):
    model = EmailAddress


class MyUserAdmin(UserAdmin):
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
