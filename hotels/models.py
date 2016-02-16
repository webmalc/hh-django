from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from colorful.fields import RGBColorField
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
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    metro_stations = models.ManyToManyField(MetroStation, blank=True)
    tariff = models.ForeignKey(Tariff, null=True, blank=True, on_delete=models.SET_NULL)
    sorting = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    def get_metro_stations_as_string(self):
        return ', '.join([str(m) for m in self.metro_stations.all()])

    get_metro_stations_as_string.short_description = 'Metro stations'

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
    name = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    photo = ProcessedImageField(upload_to='hotels_property_photos',
                                processors=[ResizeToCover(600, 600, False)],
                                format='JPEG',
                                options={'quality': 90})
    thumbnail = ImageSpecField(source='photo',
                               processors=[Thumbnail(150, 150)],
                               format='JPEG',
                               options={'quality': 90})

    property = models.ForeignKey(Property, on_delete=models.CASCADE)


class Room(CommonInfo):
    """
    Property room class
    """
    CALCULATION_TYPES = (
        ('per_person', 'За человека'),
        ('per_room', 'За комнату')

    )
    GENDER_TYPES = (
        ('mixed', 'Смешанный'),
        ('male', 'Мужской'),
        ('female', 'Женский'),

    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    calculation_type = models.CharField(max_length=20, default='per_person', choices=CALCULATION_TYPES)
    places = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=20, default='mixed', choices=GENDER_TYPES)
    price = models.PositiveIntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
