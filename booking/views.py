from django.views.generic.edit import FormView
from django.shortcuts import render_to_response
from django.conf import settings
from booking.forms import SearchForm
from hotels.models import Room
from booking.calculation import calc_commission

class SearchView(FormView):
    template_name = 'booking/search.html'
    form_class = SearchForm

    def get_initial(self):
        initial = super(SearchView, self).get_initial()
        initial.update(self.request.GET.dict())

        return initial


class SearchResultsView(FormView):
    template_name = 'booking/search_results.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        rooms = Room.objects.search(**data)[:settings.HH_SEARCH_RESULTS_PER_PAGE]
        duration = (data['end'] - data['begin']).days
        is_partner = self.request.user.is_partner()
        for room in rooms:
            room.total = room.calc_price(data['places'], duration)
            if is_partner:
                room.commission = calc_commission(room, room.total)

        return render_to_response(self.template_name, {
            'rooms': rooms, 'form': data, 'duration': duration
        })


