from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
import payments.views as views

urlpatterns = [
    # Orders out
    url(
        r'^$', permission_required('payments.add_payment', raise_exception=True)(views.PaymentsListView.as_view()),
        name='payments_list'),
    url(
        r'add/funds$', permission_required('payments.add_payment', raise_exception=True)(views.AddFundsView.as_view()),
        name='add_funds'),
    url(
        r'add/funds/(?P<pk>[0-9]+)/pay',
        permission_required('payments.add_payment', raise_exception=True)(views.BillingFormView.as_view()),
        name='billing_form')
]
