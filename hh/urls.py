"""hh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from users.views import PasswordChangeRedirectView

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'users/profile/password$', auth_views.password_change, {
        'template_name': 'users/password_change_form.html'},
        name='password_change'),
    url(r'users/profile/password/done$', PasswordChangeRedirectView.as_view(), name='password_change_done'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^booking/', include('booking.urls', namespace="booking")),
    url(r'^$', RedirectView.as_view(pattern_name='booking:search', permanent=True), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
