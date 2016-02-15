from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from colorful.fields import RGBColorField
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


class Hotel(CommonInfo, GeoMixin):
    """
    Hotel class
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    metro_stations = models.ManyToManyField(MetroStation, blank=True)
    tariff = models.ForeignKey(Tariff, null=True, blank=True, on_delete=models.SET_NULL)
    sorting = models.IntegerField(default=0)

    def get_metro_stations_as_string(self):
        return ', '.join([str(m) for m in self.metro_stations.all()])
    get_metro_stations_as_string.short_description = 'Metro stations'

    class Meta:
        permissions = (
            ("can_search_hotels", "Can search hotels"),
            ("can_book_hotels", "Can book hotels"),
            ("can_send_hotel_orders", "Can send orders to hotels"),
        )
        ordering = ['name', '-sorting']