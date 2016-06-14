from django.conf.urls import url

import payments.views as views

urlpatterns = [
    # Orders out
    url(r'$', views.PaymentsListView.as_view(), name='payments_list'),
]
