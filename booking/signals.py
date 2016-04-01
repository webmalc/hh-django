from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from booking.models import Order, OrderRoom
from users.tasks import mail_managers_task, mail_user_task, add_message_user_task
from booking.tasks import get_order_email_data


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
    created_by = order.created_by
    data = get_order_email_data(order, created)

    # Send messages & emails to user on Order completion
    if order.status == 'completed' and order.original_status != order.status:
        if order.email:
            mail_user_task.delay(
                    subject='Заявка на бронирование #{id} подтверждена'.format(id=order.id),
                    template='emails/user_booking_order_completed.html',
                    data=data,
                    email=order.email
            )
        if created_by:
            add_message_user_task.delay(
                    user_id=created_by.id,
                    template='messages/user_booking_order_completed.html',
                    data=data,
                    subject='Заявка на бронирование #{id} подтверждена'.format(id=order.id),
                    message_type='success'
            )

    # Send messages & emails to user on Order cancellation
    if order.status == 'canceled' and order.original_status != order.status:
        if order.email:
            mail_user_task.delay(
                    subject='Заявка на бронирование #{id} отменена'.format(id=order.id),
                    template='emails/user_booking_order_canceled.html',
                    data=data,
                    email=order.email
            )
        if created_by:
            add_message_user_task.delay(
                    user_id=created_by.id,
                    template='messages/user_booking_order_canceled.html',
                    data=data,
                    subject='Заявка на бронирование #{id} отменена'.format(id=order.id),
                    message_type='warning'
            )

    # Send emails to managers on Order change
    mail_managers_task.delay(
            subject='{text} заявка на бронирование #{id}'.format(
                    id=order.id, text='Новая' if created else 'Обновлена'),
            template='emails/manager_new_booking_order.html',
            data=data)


@receiver(pre_save, sender=Order, dispatch_uid="booking_order_pre_save")
def booking_order_pre_save(sender, **kwargs):
    pass
