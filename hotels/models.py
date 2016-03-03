from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from colorful.fields import RGBColorField
from django.db.models import Q
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToCover
from hh.models import CommonInfo, GeoMixin
from users.models import City


class MetroStation(CommonInfo, GeoMixin):
    """
    Metro stations
    """
    name = models.CharField(max_length=80)
    city = models.ForeignKey(City, null=True, blank=False, on_delete=models.SET_NULL)
    color = RGBColorField(null=True, blank=True)

    @classmethod
    def get_with_hotels(cls):
        ids = Room.objects.filter(is_enabled=True).values('property__metro_stations__id').distinct()
        return cls.objects.filter(id__in=ids)

    class Meta:
        ordering = ['city', 'name']


class Tariff(CommonInfo):
    """
    Hotel tariffs
    """

    def validate_is_default(is_default):
        if not is_default and not Tariff.objects.filter(is_default=True).count():
            raise ValidationError('One of the tariffs should be the default')

    name = models.CharField(max_length=80)
    is_default = models.BooleanField(default=False, verbose_name='Is default?', validators=[validate_is_default])
    minimal_commission = models.PositiveIntegerField()

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise Exception('Cannot delete default tariff')
        super(Tariff, self).delete(*args, **kwargs)


class TariffElement(models.Model):
    """
    Tariff element
    """
    PERCENT_VALIDATORS = [MaxValueValidator(100)]

    start_sum = models.PositiveIntegerField()
    end_sum = models.PositiveIntegerField()
    commission = models.PositiveIntegerField(validators=PERCENT_VALIDATORS)
    agent_commission = models.PositiveIntegerField(validators=PERCENT_VALIDATORS)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)

    def clean(self):
        if self.start_sum >= self.end_sum:
            raise ValidationError('Start sum cannot exceed end sum')


class Property(CommonInfo, GeoMixin):
    """
    Property class
    """
    TYPES = (
        ('hotel', 'отель'),
        ('hostel', 'хостел'),
        ('flat', 'квартира')
    )

    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('description'), help_text='Краткое описание отеля для поиска')
    address = models.TextField(verbose_name=_('address'))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('city'))
    metro_stations = models.ManyToManyField(MetroStation, blank=True, verbose_name=_('metro'),
                                            help_text='Ближайшие станции метро')
    tariff = models.ForeignKey(Tariff, null=True, blank=True, on_delete=models.SET_NULL)
    sorting = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True, verbose_name=_('is enabled?'))
    type = models.CharField(max_length=20, default='hotel', choices=TYPES, verbose_name=_('type'))

    def get_tariff(self):
        if self.tariff:
            return self.tariff
        else:
            return Tariff.objects.filter(is_default=True).first()

    def get_main_photo(self):
        return self.propertyphoto_set.order_by().order_by('-is_default').first()

    def get_main_photo_thumbnail(self):
        photo = self.get_main_photo()
        if photo:
            return photo.thumbnail.url
        return '/static/img/no-image.gif'

    def get_metro_stations_as_string(self):
        return ', '.join([str(m) for m in self.metro_stations.all()])

    get_metro_stations_as_string.short_description = 'Metro stations'

    def get_absolute_url(self):
        return reverse('hotel:property_change', args=[str(self.id)])

    class Meta:
        permissions = (
            ("can_search_property", "Can search property"),
            ("can_book_property", "Can book property"),
            ("can_send_property_orders", "Can send orders to property"),
        )
        ordering = ['name', '-sorting']
        verbose_name_plural = 'properties'


class PropertyPhoto(CommonInfo):
    """
    Property photo class
    """
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('title'))
    is_default = models.BooleanField(default=False, verbose_name=_('is default?'))
    photo = ProcessedImageField(upload_to='hotels_property_photos',
                                processors=[ResizeToCover(600, 600, False)],
                                format='JPEG',
                                options={'quality': 90},
                                verbose_name=_('photo')
                                )
    thumbnail = ImageSpecField(source='photo',
                               processors=[Thumbnail(120, 120)],
                               format='JPEG',
                               options={'quality': 90})

    thumbnail_xs = ImageSpecField(source='photo',
                                  processors=[Thumbnail(30, 30)],
                                  format='JPEG',
                                  options={'quality': 90})

    preview_photo = ImageSpecField(source='photo',
                                   processors=[ResizeToCover(300, 300, False)],
                                   format='JPEG',
                                   options={'quality': 90})

    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.name if self.name else 'фото #{}'.format(self.id)

    def get_absolute_url(self):
        return reverse('hotel:property_photo_change', args=[str(self.id)])

    class Meta:
        ordering = ['-is_default']


class RoomManager(models.Manager):
    """
    Rooms manager
    """

    def search(self, **kwargs):
        """
        Search for rooms
        :param kwargs: search params
        :return: models.QuerySet
        """
        q = self.all()

        if 'city' in kwargs and kwargs['city']:
            q = q.filter(property__city=kwargs['city'])

        if 'places' in kwargs and kwargs['places']:
            q = q.filter(places__gte=kwargs['places'])

        if 'type' in kwargs and kwargs['type']:
            q = q.filter(property__type=kwargs['type'])

        if 'metro_stations' in kwargs and kwargs['metro_stations'] and len(kwargs['metro_stations']):
            q = q.filter(property__metro_stations__in=kwargs['metro_stations'])

        if 'gender' in kwargs and kwargs['gender'] in ['male', 'female']:
            q = q.filter(Q(gender=kwargs['gender']) | Q(gender='mixed'))

        return q.filter(is_enabled=True).order_by('-property__sorting', 'price').distinct() \
            .select_related('property', 'property__city', 'property__tariff') \
            .prefetch_related('property__propertyphoto_set', 'property__city__metrostation_set')


class Room(CommonInfo):
    """
    Property room class
    """
    CALCULATION_TYPES = (
        ('per_person', 'За человека'),
        ('per_room', 'За номер')

    )
    GENDER_TYPES = (
        ('mixed', 'Смешанный'),
        ('male', 'Мужской'),
        ('female', 'Женский'),

    )
    total = None
    """Room total price for period"""

    objects = RoomManager()
    name = models.CharField(max_length=255, verbose_name=_('room name'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('description'), help_text='Краткое описание номера для поиска')
    calculation_type = models.CharField(max_length=20, default='per_person',
                                        choices=CALCULATION_TYPES, verbose_name=_('calculation type'))
    places = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)],
                                              verbose_name=_('places'), help_text='Количество мест/кроватей в номере')
    gender = models.CharField(max_length=20, default='mixed',
                              choices=GENDER_TYPES, verbose_name=_('room gender type'))
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('price'))
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True, verbose_name=_('is enabled?'))

    def calc_price(self, persons, duration=None, begin=None, end=None):
        """
        Calc room price for period
        :param persons: adults + children
        :param duration: days
        :param begin: datetime
        :param end: datetime
        :return: integer
        """
        if begin and end and not duration:
            duration = (end - begin).days
        if not duration:
            raise AttributeError('Duration is not defined')
        price = duration * self.price
        if self.calculation_type == 'per_person':
            price = price * persons

        return price

    def get_absolute_url(self):
        return reverse('hotel:property_room_change', args=[str(self.id)])

    class Meta:
        ordering = ['price', '-name']
