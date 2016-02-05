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


class PartnershipCommonInfo(models.Model):

    TYPES = [
        ('agent', 'Представитель агентства'),
        ('realtor', 'Частный агент/Риэлтор'),
        ('hotel_worker', 'Представитель отеля'),
        ('hotel_owner', 'Владелец отеля'),
        ('other', 'Другое'),
    ]

    patronymic = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPES)
    phone = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False)
    experience = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class PartnershipOrder(CommonInfo, PartnershipCommonInfo):
    comment = models.TextField(null=True, blank=True)


class Profile(PartnershipCommonInfo):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)

