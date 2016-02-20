from django import forms
from users.forms import CityWidget
from hotels.models import Property, Room


class RoomForm(forms.ModelForm):
    """
    Frontend room form
    """
    class Meta:
        model = Room
        fields = ['name', 'description', 'places', 'gender', 'calculation_type', 'price', 'is_enabled']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
        }


class PropertyForm(forms.ModelForm):
    """
    Frontend Property form
    """
    class Meta:
        model = Property
        fields = [
            'name', 'description', 'city', 'address', 'metro_stations', 'position', 'is_enabled'
        ]
        widgets = {
            'city': CityWidget(attrs={'class': 'not-select2'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 15}),
            'address': forms.Textarea(attrs={'rows': 2, 'cols': 15}),
        }
