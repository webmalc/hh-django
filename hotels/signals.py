from django.db.models.signals import pre_save
from django.dispatch import receiver
from hotels.models import Tariff


@receiver(pre_save, sender=Tariff, dispatch_uid="hotels_tariff_pre_save")
def users_partnership_order_post_save(sender, **kwargs):
    """
    Tariff pre save
    :param sender: Tariff
    :param kwargs: dict
    :return:
    """
    tariff = kwargs['instance']
    # Set default tariff

    if Tariff.objects.filter(is_default=True).count() and tariff.is_default:
        Tariff.objects.update(is_default=False)



