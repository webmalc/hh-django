from django.contrib.auth.decorators import permission_required
from django.conf.urls import url

import hotels.views as views

urlpatterns = [
    url(r'properties/$', permission_required('hotels.add_property', raise_exception=True)(views.PropertyList.as_view()),
        name='property_list'),
    url(r'property/add$',
        permission_required('hotels.add_property', raise_exception=True)(views.PropertyCreate.as_view()),
        name='property_create'),
    url(r'property/(?P<pk>[0-9]+)/change',
        permission_required('hotels.change_property', raise_exception=True)(views.PropertyUpdate.as_view()),
        name='property_change'),
    url(r'property/(?P<pk>[0-9]+)/rooms$',
        permission_required('hotels.add_room', raise_exception=True)(views.RoomList.as_view()),
        name='property_room_list'),
    url(r'property/(?P<pk>[0-9]+)/rooms/add$',
        permission_required('hotels.add_room', raise_exception=True)(views.RoomCreate.as_view()),
        name='property_room_create'),
    url(r'property/room/(?P<pk>[0-9]+)/change$',
        permission_required('hotels.change_room', raise_exception=True)(views.RoomUpdate.as_view()),
        name='property_room_change'),
    url(r'property/(?P<pk>[0-9]+)/photos$',
        permission_required('hotels.add_propertyphoto', raise_exception=True)(views.PhotoList.as_view()),
        name='property_photo_list'),
    url(r'property/photo/(?P<pk>[0-9]+)/delete$',
        permission_required('hotels.delete_propertyphoto', raise_exception=True)(views.PhotoDelete.as_view()),
        name='property_photo_delete'),
    url(r'property/(?P<pk>[0-9]+)/photos/add$',
        permission_required('hotels.add_propertyphoto', raise_exception=True)(views.PhotoCreate.as_view()),
        name='property_photo_create'),
    url(r'property/photo/(?P<pk>[0-9]+)/change$',
        permission_required('hotels.change_propertyphoto', raise_exception=True)(views.PhotoUpdate.as_view()),
        name='property_photo_change'),
]
