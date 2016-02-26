from django.views.generic.edit import FormView
from django.shortcuts import render_to_response
from booking.forms import SearchForm
from hotels.models import Room


class SearchView(FormView):
    template_name = 'booking/search.html'
    form_class = SearchForm


class SearchResultsView(FormView):
    template_name = 'booking/search_results.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        rooms = Room.objects.search(**data)
        return render_to_response(self.template_name, {'rooms': rooms, 'form': data})


