from __future__ import absolute_import
from hh.celery import app
from users.tasks import mail_user_task, add_message_user_task
from booking.models import Order


# TODO: close orders task

def get_order_email_data(order, created=False):
    return {
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
        'status': order.get_status_display(),
        'comment': order.comment,
        'citizenship': order.get_citizenship_display(),
        'end_time': order.ends_at.strftime('%d.%m.%Y %H:%M'),
    }


@app.task
def mail_order_hoteliers_task(order_id, subject, template, data):
    """
    Mail to order hoteliers
    :param order_id: order id
    :param subject: subject string
    :param template: template name
    :param data: data dict for template rendering
    :return: None
    """
    try:
        order = Order.objects.get(pk=order_id)
        if order.status != 'process':
            return False

        properties = {}
        for order_room in order.orderroom_set.all():
            room = order_room.room
            user = room.property.created_by
            if user.is_hotelier() and room.property.is_enabled and room.is_enabled:
                if room.property.id not in properties:
                    properties[room.property.id] = []
                properties[room.property.id].append(order_room)

        for property_id, order_rooms in properties.items():
            hotel = order_rooms[0].room.property
            additional_data = {
                'property': str(hotel),
                'order_rooms': [{'room': r.room.name, 'total': r.total} for r in order_rooms]
            }

            full_data = data.copy()
            full_data.update(additional_data)

            mail_user_task.delay(subject, template, full_data, user_id=hotel.created_by.id)
            if order.created_by:
                add_message_user_task.delay(
                        user_id=order.created_by.id,
                        template='messages/hotelier_booking_order_new.html',
                        data=full_data,
                        subject=subject,
                        message_type='info'
                )

        return True
    except Order.DoesNotExist:
        return False
