import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from hh.models import City
from hotels.models import MetroStation, Room, Property


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


class OrderPersonForm(forms.Form):
    """
    Person form for order
    """
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required': 'true'}), label=_('last name').capitalize)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'required': 'true'}), label=_('first name').capitalize)
    patronymic = forms.CharField(required=False, label=_('patronymic').capitalize)
    #citizenship = forms.ModelChoiceField(queryset=Country.objects.all(), widget=CityWithHotelsWidget, initial=347, label=_('citizenship'))


class SearchForm(forms.Form):
    """
    Hotels search form
    """
    begin = forms.DateField(
        label=_('Check-in'), initial=datetime.date.today(), widget=forms.DateInput(attrs={'required': 'true'}))

    end = forms.DateField(
        label=_('Check-out'), initial=datetime.date.today() + datetime.timedelta(days=1),
        widget=forms.DateInput(attrs={'required': 'true'}))

    places = forms.IntegerField(
        initial=1, widget=forms.NumberInput(attrs={'required': 'true', 'min': 1}),
        validators=[MinValueValidator(1)], label=_('Peoples'))

    city = forms.ModelChoiceField(
        queryset=City.get_with_hotels(), widget=CityWithHotelsWidget, initial=347, label=_('City'))

    metro_stations = forms.ModelMultipleChoiceField(queryset=MetroStation.get_with_hotels(),
                                                    widget=MetroWithHotelsWidget, required=False, label=_('Metro'))

    type = forms.ChoiceField(choices=(('', '----------'),) + Property.TYPES,
                               required=False, label=_('Type'))

    gender = forms.ChoiceField(choices=(('', '----------'),) + Room.GENDER_TYPES[1:],
                               required=False, label=_('Gender'))

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        begin = cleaned_data.get("begin")
        end = cleaned_data.get("end")

        if begin and end and (begin > end or begin < datetime.date.today()):
            raise forms.ValidationError("Dates incorrect")

        if begin == end:
            cleaned_data['end'] = begin + datetime.timedelta(days=1)

        return cleaned_data
