import datetime
from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from hh.forms import FormInitialDataMixin
from hh.widgets.month import MonthYearWidget
from payments.models import Payment


def get_datetime_now():
    return datetime.datetime.now()


class AddFundsForm(forms.ModelForm):
    """
    Payment create form
    """
    total = forms.IntegerField(
        widget=forms.NumberInput(attrs={'required': 'true', 'min': '100'}),
        initial=1000, label=_('Sum'),
        validators=[MinValueValidator(100)],
        help_text='Минимальная сумма платежа 100 руб.'
    )

    class Meta:
        model = Payment
        fields = ['total']


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
