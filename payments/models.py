from django.db import models
from hh.models import CommonInfo
from users.models import BaseUser
from booking.models import Order


class Payment(CommonInfo):
    """
    User payments
    """
    total = models.IntegerField()
    is_completed = models.BooleanField(default=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    #TODO: payment signals
