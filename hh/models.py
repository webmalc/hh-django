import pytz
from django.db import models
from sitetree.models import TreeItemBase, TreeBase
from cities_light.abstract_models import AbstractCity, AbstractRegion, AbstractCountry
from cities_light.receivers import connect_default_signals
from django.utils.translation import ugettext_lazy as _


class CommonInfo(models.Model):
    """ CommonInfo abstract model """

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False)
    created_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created_by")
    modified_by = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE, editable=False,
                                    related_name="%(app_label)s_%(class)s_modified_by")

    class Meta:
        abstract = True


class Country(AbstractCountry):
    """ HH country model."""
    pass
connect_default_signals(Country)


class Region(AbstractRegion):
    """ HH region model."""
    pass
connect_default_signals(Region)


class City(AbstractCity):
    """ HH city model."""
    TIMEZONES = [(c, c) for c in pytz.all_timezones if c.startswith('Europe') or c.startswith('Asia')]

    timezone = models.CharField(
            max_length=40, null=True, blank=True, choices=TIMEZONES
    )
    sorting = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=False, verbose_name='Is enabled?')

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

    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name='Иконка',  help_text='Иконка FontAwesome. Пример: fa-user.')
