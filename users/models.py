from django.utils.translation import ugettext_lazy as _
from hh.models import CommonInfo, City
from django.db import models
from django.contrib.auth.models import User as BaseUser, Group
from phonenumber_field.modelfields import PhoneNumberField


class User(BaseUser):
    class Meta:
        proxy = True

    def get_emails(self):
        """
        Get users emails
        :return: set()
        """
        return set([e.email for e in self.emailaddress_set.all() if e.verified] + [self.email])

    def partner_create(self):
        """
        Add user to Partner group
        """
        group = Group.objects.get(name='Partner')
        self.groups.add(group)
        self.save()

    def hotelier_create(self):
        """
        Add user to Hotelier group
        """
        profile = self.get_profile()
        group = Group.objects.get(name='Hotelier')
        if profile and profile.type in ('hotel_worker', 'hotel_owner', 'agent'):
            self.groups.add(group)
        else:
            self.groups.remove(group)
        self.save()

    def is_partner(self):
        """
        Check is user a partner
        :return: boolean
        """
        return self.groups.filter(name='Partner').exists() and self.get_profile()

    def is_hotelier(self):
        """
        Check is user a hotelier
        :return: boolean
        """
        return self.groups.filter(name='Hotelier').exists() and self.get_profile()

    def partner_remove(self):
        """
        Remove user from Partner group
        """
        if self.is_partner():
            group = Group.objects.get(name='Partner')
            group.user_set.remove(self)
            group.save()

    def get_profile(self):
        """
        Check profile
        :return: Profile
        """
        try:
            return self.profile
        except Profile.DoesNotExist:
            None

    def get_full_name(self):
        profile = self.get_profile()
        patronymic = profile.patronymic if profile else ''
        return '{0} {1} {2}'.format(self.last_name, self.first_name, patronymic)

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

    TYPES = (
        ('ooo', 'ООО',),
        ('zao', 'ЗАО',),
        ('oao', 'ОАО',),
        ('ip', 'ИП ',),
        ('other', 'Другое')
    )
    type = models.CharField(max_length=20, choices=TYPES, verbose_name='тип')
    name = models.CharField(max_length=255, verbose_name='название')

    def __str__(self):
        return '{} {}'.format(self.get_type_display(), self.name)


class PartnershipCommonInfo(models.Model):
    """
    Base Partnership information
    """
    TYPES = (
        ('agent', 'Представитель агентства'),
        ('realtor', 'Частный агент/Риэлтор'),
        ('hotel_worker', 'Представитель отеля'),
        ('hotel_owner', 'Владелец отеля'),
        ('other', 'Другое'),
    )

    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name='отчество')
    type = models.CharField(max_length=50, choices=TYPES, verbose_name='тип')
    phone = PhoneNumberField(max_length=30, verbose_name='Сотовый телефон',
                             help_text='Ваш контактный телефон. Пример: 79251234567')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='город')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    experience = models.PositiveSmallIntegerField(verbose_name='опыт',
                                                  help_text='Опыт работы в гостиничной сфере (в годах)')

    class Meta:
        abstract = True


class PartnershipOrder(CommonInfo, PartnershipCommonInfo):
    """
    Partnership information
    """
    STATUSES = (
        ('new', 'Ожидает обработки'),
        ('in_work', 'Обрабатывается'),
        ('approved', 'Принята'),
        ('canceled', 'Отклонена')
    )
    original_status = None

    def __init__(self, *args, **kwargs):
        super(PartnershipOrder, self).__init__(*args, **kwargs)
        self.original_status = self.status

    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    status = models.CharField(max_length=20, choices=STATUSES, default='new')

    def get_full_name(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.patronymic)

    class Meta:
        ordering = ['-created_at', 'status']


class Profile(PartnershipCommonInfo):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)


class UserMessage(CommonInfo):
    """
    Message for user
    """
    TYPES = (
        ('success', 'success'),
        ('info', 'info'),
        ('warning', 'warning'),
        ('danger', 'danger')
    )

    content = models.TextField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField(max_length=20, choices=TYPES, default='info')
    icon = models.CharField(max_length=50, default='fa fa-exclamation-circle')
