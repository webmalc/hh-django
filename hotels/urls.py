from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

import hotels.views as views

urlpatterns = [
    url(r'properties/$', permission_required('hotels.add_property', raise_exception=True)(views.PropertyList.as_view()),
        name='property_list'),
    url(r'property/add$', permission_required('hotels.add_property', raise_exception=True)(views.PropertyCreate.as_view()),
        name='property_create'),
]
