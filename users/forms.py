from django import forms
from users.models import PartnershipOrder, Organization


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
          'comment': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class OrganizationForm(forms.ModelForm):
    """
    Frontend OrganizationForm
    """
    class Meta:
        model = Organization
        fields = ['type', 'name']
