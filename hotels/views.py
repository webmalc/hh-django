from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from hotels.models import Property
from hotels.forms import PropertyForm


class PropertyList(ListView):
    """
    User properties list
    """
    model = Property

    def dispatch(self, request, *args, **kwargs):
        if not request.user.hotels_property_created_by.count():
            return redirect('hotel:property_create')
        return super(PropertyList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super(PropertyList, self).get_queryset().\
            filter(created_by=self.request.user).prefetch_related('metro_stations', 'propertyphoto_set', 'room_set')


class PropertyCreate(CreateView):
    """
    User property create
    """
    form_class = PropertyForm
    template_name = 'hotels/property_edit.html'

