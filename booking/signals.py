from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from booking.models import Order
from users.tasks import mail_managers_task, mail_user_task
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
    email_data = get_order_email_data(order, created)

    # Send emails to user on Order completion
    if order.email and order.status == 'completed' and order.original_status != order.status:
        mail_user_task.delay(
                subject='Заявка на бронирование #{id} подтверждена'.format(id=order.id),
                template='emails/user_booking_order_completed.html',
                data=email_data,
                email=order.email
        )

    # Send emails to user on Order cancellation
    if order.email and order.status == 'canceled' and order.original_status != order.status:
        mail_user_task.delay(
            subject='Заявка на бронирование #{id} отменена'.format(id=order.id),
            template='emails/user_booking_order_canceled.html',
            data=email_data,
            email=order.email
        )

    # Send emails to managers on Order change
    mail_managers_task.delay(
            subject='{text} заявка на бронирование #{id}'.format(
                    id=order.id, text='Новая' if created else 'Обновлена'),
            template='emails/manager_new_booking_order.html',
            data=email_data)


@receiver(pre_save, sender=Order, dispatch_uid="booking_order_pre_save")
def booking_order_pre_save(sender, **kwargs):
    pass
