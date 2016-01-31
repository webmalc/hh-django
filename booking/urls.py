from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

import booking.views as views

urlpatterns = [
    url(r'search/$', views.SearchView.as_view(), name='search'),
]
