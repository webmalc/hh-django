import pytz
from django.contrib import messages
from django.db import models
from sitetree.models import TreeItemBase, TreeBase
from cities_light.abstract_models import AbstractCity, AbstractRegion, AbstractCountry
from cities_light.receivers import connect_default_signals
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField


class DeleteSuccessMessageMixin(object):
    """
    Adds a success message on successful object deletion.
    """
    success_message = ''

    def delete(self, request, *args, **kwargs):
        success_message = self.success_message
        if success_message:
            messages.success(self.request, success_message)
        return super(DeleteSuccessMessageMixin, self).delete(request, *args, **kwargs)


class GeoMixin(models.Model):
    """
    GeoMixin: add Latitude & Longitude fields
    """
    position = GeopositionField(null=True, blank=True, verbose_name=_('coordinates'))
    latitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.position:
            self.latitude = self.position.latitude
            self.longitude = self.position.longitude
        super(GeoMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CommonInfo(models.Model):
    """ CommonInfo abstract model """

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    created_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created_by")
    modified_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE, editable=False,
                                    related_name="%(app_label)s_%(class)s_modified_by")

    def __str__(self):
        return getattr(self, 'name', '{} #{}'.format(type(self).__name__, str(self.id)))

    class Meta:
        abstract = True


class CityMixin:
    """
    City, Region, County name mixin
    """
    def get_first_alternate_name(self):
        """
        Returns first alternate name
        :return: string
        """
        return self.alternate_names.split(',')[0]
    get_first_alternate_name.short_description = 'Alternative name'
    get_first_alternate_name.admin_order_field = 'alternate_names'

    def __str__(self):
        name = self.get_first_alternate_name()
        return name if name else self.name


class Country(CityMixin, AbstractCountry):
    """ HH country model."""
    class Meta:
        ordering = ['name']
connect_default_signals(Country)


class Region(CityMixin, AbstractRegion):

    """ HH region model."""
    def get_display_name(self):
        return '%s, %s' % (self, self)

connect_default_signals(Region)


class City(CityMixin, AbstractCity):
    """ HH city model."""
    TIMEZONES = [(c, c) for c in pytz.all_timezones if c.startswith('Europe') or c.startswith('Asia')]

    timezone = models.CharField(
            max_length=40, null=True, blank=True, choices=TIMEZONES
    )
    sorting = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=False, verbose_name='Is enabled?')

    def get_display_name(self):
        if self.region_id:
            return '%s, %s, %s' % (self, self.region, self.country)
        else:
            return '%s, %s' % (self.name, self.country)

    @classmethod
    def get_with_hotels(cls):
        from hotels.models import Room
        ids = Room.objects.filter(is_enabled=True).values('property__city_id').distinct()
        return cls.objects.filter(is_enabled=True, id__in=ids)

    class Meta:
        ordering = ['-sorting', 'name']
        unique_together = (('region', 'name'), ('region', 'slug'))
        verbose_name_plural = _('cities')
connect_default_signals(City)


class SiteTreeTree(TreeBase):
    """ HH tree model."""
    pass


class SiteTreeItem(TreeItemBase):
    """ HH tree item model."""

    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='Иконка',
                            help_text='Иконка FontAwesome. Пример: fa-user.')
