from django.db import models
from django.conf import settings
from django.utils.timezone import timedelta, datetime, now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from hh.models import CommonInfo
from hotels.models import Room


class OrderManager(models.Manager):
    """
    OrderManager manager
    """
    def user_can_booking(self, user):
        """
        Check user order limit
        :param user
        """
        query = self.all().filter(created_by=user)

        if query.count() and not user.is_partner():
            last_order = query.latest('created_at')
            time_limit = settings.HH_BOOKING_ORDER_TIME_LIMIT
            if last_order.created_at + timedelta(minutes=time_limit) > now():
                return False

        limit = settings.HH_BOOKING_ORDER_PARTNER_LIMIT if user.is_partner() else settings.HH_BOOKING_ORDER_USER_LIMIT
        if query.filter(status='process').count() >= limit:
            return False

        return True

    def filter_for_hotelier(self, user, query=None):
        """
        Filter Orders for hotelier
        :param user: user
        :type user: user.User
        :param query: query
        :type query: QuerySet or None
        :return: filtered QuerySet
        :rtype: QuerySet
        """
        if 1 or query is None:
            query = self.all()
        hotels = user.hotels_property_created_by.all()

        return query.filter(order_rooms__room__property__in=hotels).distinct()


def get_order_ends_at_datetime():
    return datetime.now() + timedelta(minutes=settings.HH_BOOKING_ORDER_LIFETIME)


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
    STATUSES_INFO = {
        'process': {'icon': 'fa fa-spin fa-spinner', 'class': 'default'},
        'completed': {'icon': 'fa fa-check', 'class': 'success'},
        'canceled': {'icon': 'fa fa-ban', 'class': 'danger'}
    }

    PERCENT_VALIDATORS = [MaxValueValidator(100)]

    objects = OrderManager()
    original_status = None

    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
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
            default=get_order_ends_at_datetime)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.original_status = self.status

    def get_fio(self):
        """
        Get full name
        :return: full name string string
        """
        return '{} {} {}'.format(self.last_name, self.first_name, self.patronymic)
    get_fio.short_description = 'fio'

    def get_commission_sum(self):
        """
        Get commission sum
        :return: int
        """
        if self.total:
            return int(self.total * self.commission / 100)
        return 0
    get_commission_sum.short_description = 'commission sum'

    def get_agent_commission_sum(self):
        """
        Get agent commission sum
        :return: int
        """
        return int(self.get_commission_sum() * self.agent_commission / 100)
    get_agent_commission_sum.short_description = 'agent commission sum'

    def get_duration(self):
        """
        :return (int) duration in days or None
        """
        if self.end and self.begin:
            return (self.end - self.begin).days
        return None

    def get_property(self):
        """
        Get accepted room property
        :return: hotels.model.Property
        """
        if self.accepted_room:
            return self.accepted_room.property
        return None
    get_property.short_description = 'property'

    def get_full_name(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.patronymic)

    def get_status_info(self):
        """
        Return status dict for order
        """
        return self.STATUSES_INFO[self.status]

    def clean(self):
        if self.begin and self.end and (self.begin > self.end):
            raise ValidationError('Dates incorrect')

        if self.begin and self.end and self.begin == self.end:
            self.end = self.begin + timedelta(days=1)

    class Meta:
        ordering = ['-created_at', 'status']


class OrderRoom(models.Model):
    """
    Booking order room class
    """
    room = models.ForeignKey(Room, verbose_name=_('room'))
    total = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('total'))
    order = models.ForeignKey(Order, verbose_name=_('order'), related_name='order_rooms')
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

    class Meta:
        ordering = ['-is_accepted']

