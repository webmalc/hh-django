from django import forms
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from users.models import City
from hotels.models import MetroStation, Room


class CityWithHotelsWidget(ModelSelect2Widget):
    queryset = City.get_with_hotels()
    search_fields = [
        'name__icontains', 'alternate_names__icontains'
    ]
    attrs = {'class': 'not-select2'}


class MetroWithHotelsWidget(ModelSelect2MultipleWidget):
    queryset = MetroStation.get_with_hotels()
    search_fields = [
        'name__icontains',
    ]
    attrs = {'class': 'not-select2'}


class SearchForm(forms.Form):
    """
    Hotels search form
    """

    # Fields
    places = forms.IntegerField(initial=1)
    city = forms.ModelChoiceField(queryset=City.get_with_hotels(), widget=CityWithHotelsWidget, initial=347)
    metro_stations = forms.ModelMultipleChoiceField(queryset=MetroStation.get_with_hotels(),
                                                    widget=MetroWithHotelsWidget)
    gender = forms.ChoiceField(choices=Room.GENDER_TYPES, required=True)
    # metro_stations, gender, prices
