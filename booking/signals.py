from django.db.models.signals import pre_save, post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from booking.models import Order
from users.tasks import mail_managers_task, mail_user_task
from booking.tasks import mail_order_hoteliers_task


@receiver(post_save, sender=Order, dispatch_uid="booking_order_post_save")
def booking_order_post_save(sender, **kwargs):
    """
    Order post_save signal
    :param sender: booking.models.Order
    :param kwargs: dict
    :return: None
    """
    order = kwargs['instance']
    created = kwargs['created']
    email_data = {
        'id': order.id,
        'begin': order.begin.strftime('%d.%m.%Y'),
        'end': order.end.strftime('%d.%m.%Y'),
        'fio': order.get_fio(),
        'places': order.places,
        'phone': str(order.phone),
        'total': order.total,
        'commission': order.get_agent_commission_sum(),
        'agent_commission': order.get_agent_commission_sum(),
        'is_agent': order.is_agent_order,
        'is_new': created,
        'room': '{}, {}'.format(order.accepted_room.property, order.accepted_room) if order.accepted_room else None,
        'property': str(order.accepted_room.property) if order.accepted_room else None,
        'address': '{}, {}'.format(order.accepted_room.property.city,
                                   order.accepted_room.property.address) if order.accepted_room else None,
        'property_phone': str(order.accepted_room.property.created_by.profile.phone) if order.accepted_room else None,
        'status': order.get_status_display()
    }

    # Send emails to user on Order completion
    """if order.email and order.status == 'completed' and order.original_status != order.status:
        mail_user_task.delay(
                subject='Заявка на бронирование #{id} подтверждена'.format(id=order.id),
                template='emails/user_booking_order_completed.html',
                data=email_data,
                email=order.email
        )"""

    # Send emails to hoteliers
    if True or created:
        mail_order_hoteliers_task(
            order_id=order.id,
            subject='Новая заявка на бронирование #{id}'.format(id=order.id),
            template='emails/hotelier_booking_order_new.html',
            data=email_data,
        )

    # Send emails to managers on Order change
    """mail_managers_task.delay(
            subject='{text} заявка на бронирование #{id}'.format(
                    id=order.id, text='Новая' if created else 'Обновлена'),
            template='emails/manager_new_booking_order.html',
            data=email_data)"""


@receiver(pre_save, sender=Order, dispatch_uid="booking_order_pre_save")
def booking_order_pre_save(sender, **kwargs):
    pass
