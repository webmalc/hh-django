from django.conf.urls import url

import booking.views as views

urlpatterns = [
    url(r'search/$', views.SearchView.as_view(), name='search'),
    url(r'search/results$', views.SearchResultsView.as_view(), name='search_results'),
]
