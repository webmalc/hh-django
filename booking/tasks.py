from __future__ import absolute_import
from hh.celery import app
from users.tasks import mail_user_task
from booking.models import Order


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
            }
            full_data = data.copy()
            full_data.update(additional_data)

            mail_user_task(subject, template, full_data, user_id=hotel.created_by.id)

        return True
    except Order.DoesNotExist:
        return False



