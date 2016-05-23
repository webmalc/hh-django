from django.db import models
from hh.models import CommonInfo
from users.models import User
from booking.models import Order
from django.db.models import Sum


class PaymentManager(models.Manager):
    """
    PaymentManager manager
    """
    def calc_for_user(self, user):
        """
        :param user: user.models.User
        :type user: user.models.User
        :return: user wallet balance
        :rtype: int
        """
        r = self.all().filter(user=user, is_completed=True).aggregate(Sum('total'))

        return r['total__sum'] if r['total__sum'] else 0


class Payment(CommonInfo):
    """
    User payments
    """
    total = models.IntegerField()
    is_completed = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    objects = PaymentManager()

    class Meta:
        ordering = ['-created_at']
