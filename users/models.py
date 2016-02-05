from django.utils.translation import ugettext_lazy as _
import re
from hh.models import CommonInfo, City
from django.db import models
from django.contrib.auth.models import User as BaseUser


class User(BaseUser):
    class Meta:
        proxy = True

    def __str__(self):

        if self.first_name:
            return '%s %s' % (self.last_name, self.first_name)
        elif self.email:
            return '%s' % self.email
        else:
            return '%s' % self.username


class Organization(CommonInfo):
    """
    Organization model
    """

    TYPES = {
        'ooo': 'ООО',
        'zao': 'ЗАО',
        'oao': 'ОАО',
        'ip': 'ИП ',
        'other': 'Другое'
    }
    type = models.CharField(max_length=20, choices=TYPES.items())
    name = models.CharField(max_length=255)

    def get_type_name(self):
        return self.TYPES[self.type]

    def __str__(self):
        return '{} {}'.format(self.get_type_name(), self.name)


class PartnershipCommonInfo(models.Model):
    """
    Base Partnership information
    """
    TYPES = {
        'agent': 'Представитель агентства',
        'realtor': 'Частный агент/Риэлтор',
        'hotel_worker': 'Представитель отеля',
        'hotel_owner': 'Владелец отеля',
        'other': 'Другое',
    }

    patronymic = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, choices=sorted(TYPES.items()))
    phone = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=False)
    experience = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        """
        Model save override
        :param args:
        :param kwargs:
        :return:
        """
        self.phone = re.sub(r'\D', '', self.phone)
        super(PartnershipCommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PartnershipOrder(CommonInfo, PartnershipCommonInfo):
    """
    Base Partnership information
    """
    STATUSES = {
        'new': 'Ожидает обработки',
        'in_work': 'Обрабатывается',
        'approved': 'Принята',
        'canceled': 'Отклонена'
    }

    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES.items(), default='new')

    def get_full_name(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.patronymic)


class Profile(PartnershipCommonInfo):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

