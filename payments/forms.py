import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from hh.forms import FormInitialDataMixin
from hh.widgets.month import MonthYearWidget


def get_datetime_now():
    return datetime.datetime.now()


class PaymentsFilterForm(forms.Form, FormInitialDataMixin):
    TYPES = (
        ('', '----------'),
        ('in', 'Поступление'),
        ('out', 'Расход'),
    )

    date = forms.DateField(
        widget=MonthYearWidget(attrs={'required': 'true'}), initial=get_datetime_now, label=_('Period'))
    payment_type = forms.ChoiceField(choices=TYPES, required=False, label=_('type').capitalize())
    is_send = forms.CharField(widget=forms.HiddenInput, initial=1)
