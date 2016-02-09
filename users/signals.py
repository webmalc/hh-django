from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import PartnershipOrder
from users.tasks import mail_managers_task, mail_user_task


@receiver(post_save, sender=PartnershipOrder, dispatch_uid="users_partnership_order_post_save")
def users_partnership_order_post_save(sender, **kwargs):
    """
    PartnershipOrder pre save
    :param sender: PartnershipOrder
    :param kwargs: dict
    :return:
    """
    order = kwargs['instance']
    user = order.created_by
    created = kwargs['created']

    # Save order to user profile
    if not created and order.original_status != order.status \
            and order.status == 'approved' and user:

        for field in ('first_name', 'last_name'):
            setattr(user, field, getattr(order, field, getattr(user, field)))

        for field in ('patronymic', 'type', 'phone', 'city', 'organization', 'experience'):
            setattr(user.profile, field, getattr(order, field, getattr(user.profile, field)))

        user.partner_create()
        user.profile.save()
        user.save()

        mail_user_task.delay(
            subject='Заявка на партнерство #{} подтверждена'.format(order.id),
            template='emails/user_partner_order_approved.html',
            data={'id': order.id},
            user_id=user.id
        )

    # Send emails to user on PartnershipOrder cancel
    if not created and order.original_status != order.status \
            and order.status == 'canceled' and user:

        mail_user_task.delay(
            subject='Заявка на партнерство #{} отклонена'.format(order.id),
            template='emails/user_partner_order_canceled.html',
            data={'id': order.id},
            user_id=user.id
        )

    # Send emails to managers on PartnershipOrder create
    if created:
        mail_managers_task.delay(
                subject='Новая заявка на партнерство #{}'.format(order.id),
                template='emails/manager_new_partner_order.html',
                data={
                    'id': order.id,
                    'full_name': order.get_full_name(),
                    'phone': order.phone,
                    'city': str(order.city),
                    'type': order.get_type_display(),
                    'organization': str(order.organization),
                    'comment': order.comment,
                })
