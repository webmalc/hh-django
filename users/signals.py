from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import PartnershipOrder
from users.tasks import mail_managers_task


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
        mail_managers_task.delay(
                subject='Новая заявка на партнерство # {}'.format(order.id),
                template='emails/new_partner_order.html',
                data={
                    'id': order.id,
                    'full_name': order.get_full_name(),
                    'phone': order.phone,
                    'city': str(order.city),
                    'type': order.get_type_display(),
                    'organization': str(order.organization),
                    'comment': order.comment,
                })
