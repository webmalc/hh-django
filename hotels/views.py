from django.views.generic import ListView
from hotels.models import Property


class PropertyList(ListView):

    model = Property

    def get_queryset(self):
        return super(PropertyList, self).get_queryset().\
            filter(created_by=self.request.user).prefetch_related('metro_stations', 'propertyphoto_set', 'room_set')

