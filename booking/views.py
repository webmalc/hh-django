from django.views.generic.edit import FormView
from booking.forms import SearchForm


class SearchView(FormView):
    template_name = 'booking/search.html'
    form_class = SearchForm

