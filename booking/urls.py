from django.conf.urls import url

import booking.views as views

urlpatterns = [
    url(r'search/$', views.SearchView.as_view(), name='search'),
    url(r'search/results$', views.SearchResultsView.as_view(), name='search_results'),
    url(r'order/create$', views.OrderCreateView.as_view(), name='order_create'),
    url(r'order/create/success$', views.OrderCreateSuccessView.as_view(), name='order_create_success'),
]
