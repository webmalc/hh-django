from django.db import models
from django.conf import settings
from django.utils.timezone import timedelta, datetime, localtime
from django.core.exceptions import ValidationError
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

    original_status = None

    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('first name'))
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('patronymic'))
    citizenship = models.CharField(
            max_length=100, choices=CITIZENSHIP_TYPES, default='rus', verbose_name=_('citizenship')
    )
    phone = PhoneNumberField(max_length=30, verbose_name=_('mobile phone'))
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=_('e-mail'))
    begin = models.DateField(verbose_name=_('Check-in'))
    end = models.DateField(verbose_name=_('Check-out'))
    places = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    total = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)], verbose_name=_('total'))
    commission = models.PositiveIntegerField(
            default=0, validators=PERCENT_VALIDATORS, verbose_name=_('commission'))
    agent_commission = models.PositiveIntegerField(
            default=0, validators=PERCENT_VALIDATORS, verbose_name=_('agent commission'))
    is_agent_order = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUSES, default='process', verbose_name=_('status'))
    accepted_room = models.ForeignKey(
            Room, null=True, blank=True, verbose_name=_('room'), related_name='%(class)s_accepted_room'
    )
    comment = models.TextField(null=True, blank=True, verbose_name=_('comment'))
    ends_at = models.DateTimeField(
            verbose_name=_('ends at'),
            default=datetime.now() + timedelta(minutes=settings.HH_BOOKING_ORDER_LIFETIME))

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.original_status = self.status

    def get_fio(self):
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)
    get_fio.short_description = 'fio'

    def get_commission_sum(self):
        if self.total:
            return int(self.total * self.commission / 100)
        return 0
    get_commission_sum.short_description = 'commission sum'

    def get_agent_commission_sum(self):
        return int(self.get_commission_sum() * self.agent_commission / 100)
    get_agent_commission_sum.short_description = 'agent commission sum'

    def get_property(self):
        if self.accepted_room:
            return self.accepted_room.property
        return None
    get_property.short_description = 'property'

    def clean(self):
        if self.begin and self.end and (self.begin > self.end):
            raise ValidationError('Dates incorrect')

        if self.begin == self.end:
            self.end = self.begin + timedelta(days=1)

    class Meta:
        ordering = ['-created_at', 'status']


class OrderRoom(models.Model):
    """
    Booking order room class
    """
    room = models.ForeignKey(Room, verbose_name=_('room'))
    total = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('total'))
    order = models.ForeignKey(Order, verbose_name=_('order'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('is accepted'))

    def get_property(self):
        return self.room.property
    get_property.short_description = 'property'

    def delete(self, *args, **kwargs):
        if self.is_accepted:
            raise Exception('Cannot delete accepted room')
        super(OrderRoom, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(OrderRoom, self).save(*args, **kwargs)

        if self.is_accepted and not self.order.accepted_room:
            self.order.accepted_room = self.room
            self.order.save()

