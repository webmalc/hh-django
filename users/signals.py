from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import PartnershipOrder
from hh.messangers.mailer import Mailer


@receiver(post_save, sender=PartnershipOrder, dispatch_uid="users_partnership_order_post_save")
def users_partnership_order_post_save(sender, **kwargs):
    """
    Save PartnershipOrder to user profile
    :param sender: PartnershipOrder
    :param kwargs: dict
    :return:
    """
    order = kwargs['instance']
    user = order.created_by
    created = kwargs['created']
    if not created and order.original_status != order.status \
            and order.status == 'approved' and user:

        for field in ('first_name', 'last_name'):
            setattr(user, field, getattr(order, field, getattr(user, field)))

        for field in ('patronymic', 'type', 'phone', 'city', 'organization', 'experience'):
            setattr(user.profile, field, getattr(order, field, getattr(user.profile, field)))

        user.profile.save()
        user.save()

    if created:
        # Send emails to managers on PartnershipOrder create
        Mailer.mail_managers(
            subject='Новая заявка на партнерство # {}'.format(order.id),
            template='emails/new_partner_order.html',
            data={'order': order}
        )
