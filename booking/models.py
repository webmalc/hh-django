from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from hh.models import CommonInfo
from hotels.models import Room


class Order(CommonInfo):
    """
    Booking order class
    """
    CITIZENSHIP_TYPES = (
        ('rus', 'Россия'),
        ('sng', 'СНГ'),
        ('eu', 'Европа'),
        ('usa', 'США'),
        ('other', 'Другое')

    )
    STATUSES = (
        ('process', 'Обрабатывается'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена')

    )
    PERCENT_VALIDATORS = [MaxValueValidator(100)]

    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('first name'))
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('patronymic'))
    citizenship = models.CharField(
            max_length=100, choices=CITIZENSHIP_TYPES, default='rus', verbose_name=_('citizenship')
    )
    phone = PhoneNumberField(max_length=30, verbose_name=_('mobile phone'))
    begin = models.DateField(verbose_name=_('Check-in'))
    end = models.DateField(verbose_name=_('Check-out'))
    places = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    total = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('total'))
    commission = models.PositiveIntegerField(
            default=0, validators=PERCENT_VALIDATORS, verbose_name=_('commission'))
    agent_commission = models.PositiveIntegerField(
            default=0, validators=PERCENT_VALIDATORS, verbose_name=_('agent commission'))
    is_agent_order = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUSES, default='process', verbose_name=_('status'))
    rooms = models.ManyToManyField(Room, verbose_name=_('rooms'))
    accepted_room = models.ForeignKey(
            Room, null=True, blank=False, verbose_name=_('room'), related_name='%(class)s_accepted_room'
    )
    comment = models.TextField(null=True, blank=True, verbose_name=_('comment'))

    def get_fio(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)
    get_fio.short_description = 'fio'

    class Meta:
        ordering = ['-created_at', 'status']
