from django.views.generic import ListView
from payments.models import Payment
from payments.forms import PaymentsFilterForm
from hh.utils import get_month_day_range


class PaymentsListView(ListView):
    """
    Payments list
    """
    template_name = 'payments/payments_list.html'
    model = Payment

    def get_context_data(self, **kwargs):
        context = super(PaymentsListView, self).get_context_data(**kwargs)
        context['filter_form'] = PaymentsFilterForm(self.request.GET if self.request.GET.get('is_send', None) else None)
        return context

    def get_queryset(self):
        form = PaymentsFilterForm(self.request.GET if self.request.GET.get('is_send', None) else None)
        date = form.cleaned_data['date'] if form.is_valid() else form.get_initial_data()['date']()
        payment_type = form.cleaned_data['payment_type'] if form.is_valid() else None
        q = super(ListView, self).get_queryset()

        if payment_type and payment_type == 'in':
            q = q.filter(total__gte=0)
        if payment_type and payment_type == 'out':
            q = q.filter(total__lt=0)

        return q.filter(user=self.request.user, created_at__range=get_month_day_range(date))
