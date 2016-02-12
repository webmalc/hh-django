from django import forms
from django_select2.forms import ModelSelect2Widget
from users.models import PartnershipOrder, Organization, City


class CityWidget(ModelSelect2Widget):
    queryset = City.objects.filter(is_enabled=True)
    search_fields = [
        'name__icontains', 'alternate_names__icontains'
    ]
    attrs = {'class': 'not-select2'}


class PartnershipOrderForm(forms.ModelForm):
    """
    Frontend PartnershipOrderForm
    """
    class Meta:
        model = PartnershipOrder
        fields = [
            'last_name', 'first_name', 'patronymic', 'type', 'phone', 'city', 'experience', 'comment'
        ]
        widgets = {
            'city': CityWidget(attrs={'class': 'not-select2'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class OrganizationForm(forms.ModelForm):
    """
    Frontend OrganizationForm
    """
    class Meta:
        model = Organization
        fields = ['type', 'name']
