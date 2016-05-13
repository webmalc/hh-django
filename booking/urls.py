from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

import booking.views as views

urlpatterns = [
    url(r'search/$', views.SearchView.as_view(), name='search'),
    url(r'search/results$', views.SearchResultsView.as_view(), name='search_results'),
    url(r'order/create$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'order/create/success$', views.OrderCreateSuccessView.as_view(), name='order_create_success'),

    # Orders out
    url(r'orders/out/active', views.OutActiveOrdersView.as_view(), name='orders_out_active_list'),
    url(r'orders/out/completed', views.OutCompletedOrdersView.as_view(), name='orders_out_completed_list'),
    url(r'order/(?P<pk>[0-9]+)/cancel', views.order_cancel, name='order_cancel'),
    url(r'order/(?P<pk>[0-9]+)/confirmation/(?P<order_room_id>[0-9]+)', views.order_confirmation, name='order_confirmation'),

    # Orders in
    url(r'orders/in/active',
        permission_required('hotels.can_book_property', raise_exception=True)(views.InActiveOrdersView.as_view()),
        name='orders_in_active_list'),
    url(r'orders/in/completed',
        permission_required('hotels.can_book_property', raise_exception=True)(views.InCompletedOrdersView.as_view()),
        name='orders_in_completed_list'),
]
