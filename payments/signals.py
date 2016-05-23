from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from payments.models import Payment


@receiver(post_save, sender=Payment, dispatch_uid="booking_order_post_save")
@receiver(post_delete, sender=Payment, dispatch_uid="booking_order_post_delete")
def calc_user_wallet_balance(sender, **kwargs):
    """
    Calc user wallet balance
    :param sender: payments.models.Payment
    :param kwargs: dict
    :return: None
    """
    payment = kwargs['instance']
    profile = payment.user.get_profile()

    if profile:
        profile.wallet_balance = Payment.objects.calc_for_user(payment.user)
        profile.save()