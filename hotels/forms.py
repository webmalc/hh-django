from django import forms
from users.forms import CityWidget
from hotels.models import Property


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
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }
