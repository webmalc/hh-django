from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.core.urlresolvers import reverse_lazy
from booking.forms import SearchForm, OrderPersonForm
from booking.models import Order
from hotels.models import Room
from booking.calculation import calc_commission


class SearchView(FormView):
    """
    Search form view
    """
    template_name = 'booking/search.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['max_rooms'] = settings.HH_BOOKING_MAX_ORDER_ROOMS
        return context

    def get_initial(self):
        initial = super(SearchView, self).get_initial()
        initial.update(self.request.GET.dict())

        return initial


class SearchResultsView(FormView):
    """
    Search results view
    """
    template_name = 'booking/search_results.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        rooms = Room.objects.search(**data)[:settings.HH_SEARCH_RESULTS_PER_PAGE]
        duration = (data['end'] - data['begin']).days
        is_partner = self.request.user.is_partner()

        for room in rooms:
            room.total = room.calc_price(data['places'], duration)
            if is_partner:
                room.commission = calc_commission(room, room.total)

        return render_to_response(self.template_name, {
            'rooms': rooms,
            'form': data,
            'duration': duration,
            'order_lifetime': settings.HH_BOOKING_ORDER_LIFETIME,
            'can_booking': Order.objects.user_can_booking(user)
        }, RequestContext(self.request))


class OrderCreateSuccessView(TemplateView):
    """
    Order success message
    """
    template_name = 'booking/order_person_form_success.html'


class OrderCreateView(FormView):
    """
    Order creation form view
    """
    form_class = OrderPersonForm
    template_name = 'booking/order_person_form.html'

    def get_success_url(self):
        return reverse_lazy('booking:order_create_success')

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(OrderCreateView, self).get_initial()
        user = self.request.user

        try:
            last_order = Order.objects.filter(created_by=self.request.user).latest('created_at')
            data = model_to_dict(last_order, exclude={'comment'})
        except Order.DoesNotExist:
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        initial.update(data)
        return initial

    def form_valid(self, form):
        error_response = render_to_response('booking/order_person_form_error.html')

        if not Order.objects.user_can_booking(self.request.user):
            return error_response

        rooms = self.request.POST.get('rooms', [])
        if len(rooms) > settings.HH_BOOKING_MAX_ORDER_ROOMS or len(rooms) == 0:
            return error_response

        order = form.instance
        order.places = self.request.POST['places']
        order.begin = self.request.POST['begin']
        order.end = self.request.POST['end']
        try:
            order.full_clean()
            order.save()
        except ValidationError:
            return error_response
        return super(OrderCreateView, self).form_valid(form)
