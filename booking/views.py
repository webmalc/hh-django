from django.views.generic.edit import FormView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from booking.forms import SearchForm, OrderPersonForm
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
        order_form = OrderPersonForm
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
            'order_form': order_form,
            'duration': duration,
            'order_lifetime': settings.HH_BOOKING_ORDER_LIFETIME,
        }, RequestContext(self.request))


