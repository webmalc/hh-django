from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from payments.models import Payment
from payments.forms import PaymentsFilterForm, AddFundsForm
from hh.utils import get_month_day_range
from payments.rbk import Rbk


@csrf_exempt
def check_payment(request):
    """
    Payment verification
    :param request: request
    :type request: django.http.HttpRequest
    :return: response
    :rtype: django.http.HttpResponse | django.http.HttpResponseNotFound
    """
    if Rbk.process_request(request):
        return HttpResponse('OK')
    else:
        return HttpResponseNotFound('FAIL')


class AddFundsView(CreateView):
    """
    Add payment form billing system
    """
    model = Payment
    template_name = 'payments/add_funds.html'
    form_class = AddFundsForm

    def get_success_url(self):
        return reverse_lazy('payments:billing_form', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.user = self.request.user
        payment.is_completed = False
        payment.comment = "Пополнение счета HostelHunt"
        return super(AddFundsView, self).form_valid(form)


class BillingFormView(DetailView):
    """
    Billing form view
    """
    model = Payment
    template_name = 'payments/billing_form.html'

    def get_context_data(self, **kwargs):
        context = super(BillingFormView, self).get_context_data(**kwargs)
        context['form_data'] = Rbk.get_form_data(context['payment'])

        return context

    def get_queryset(self):
        q = super(BillingFormView, self).get_queryset()
        return q.filter(is_completed=False, user=self.request.user)


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
