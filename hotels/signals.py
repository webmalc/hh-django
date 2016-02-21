import os
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from hotels.models import Tariff, Property, Room, PropertyPhoto
from users.tasks import mail_managers_task


@receiver(pre_delete, sender=PropertyPhoto, dispatch_uid="hotels_property_photo_pre_delete")
def hotels_property_photo_pre_delete(sender, **kwargs):
    """
    PropertyPhoto pre delete
    :param sender: PropertyPhoto
    :param kwargs: dict
    :return:
    """
    photo = kwargs['instance']
    # Remove files
    if os.path.isfile(photo.thumbnail.path):
        os.remove(photo.thumbnail.path)
    photo.photo.delete(save=False)


@receiver(post_save, sender=PropertyPhoto, dispatch_uid="hotels_property_photo_post_save")
def hotels_property_photo_post_save(sender, **kwargs):
    """
    PropertyPhoto post save
    :param sender: PropertyPhoto
    :param kwargs: dict
    :return:
    """
    photo = kwargs['instance']

    email_data = {
        'id': photo.id,
        'name': photo.name,
        'hotel': str(photo.property),
    }
    email_template = 'emails/manager_property_photo_save.html'
    mail_managers_task.delay(
                subject='Сохранено фото #{id} у отеля <{hotel}>'.format(id=photo.id, hotel=photo.property),
                template=email_template,
                data=email_data
        )


@receiver(pre_save, sender=PropertyPhoto, dispatch_uid="hotels_property_photo_pre_save")
def hotels_property_photo_pre_save(sender, **kwargs):
    """
    PropertyPhoto pre save
    :param sender: PropertyPhoto
    :param kwargs: dict
    :return:
    """
    photo = kwargs['instance']
    # Set default photo
    if PropertyPhoto.objects.filter(is_default=True).count() and photo.is_default:
        PropertyPhoto.objects.update(is_default=False)


@receiver(pre_save, sender=Tariff, dispatch_uid="hotels_tariff_pre_save")
def hotels_tariff_pre_save(sender, **kwargs):
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


@receiver(post_save, sender=Property, dispatch_uid="hotels_property_post_save")
def hotels_property_post_save(sender, **kwargs):
    """
    Property post save
    :param sender: Tariff
    :param kwargs: dict
    :return:
    """
    hotel = kwargs['instance']
    created = kwargs['created']
    email_data = {
        'id': hotel.id,
        'name': hotel.name,
        'description': str(hotel.description),
        'city': str(hotel.city),
        'address': hotel.address,
        'user': hotel.created_by.username
    }
    email_template = 'emails/manager_property_save.html'

    # Send emails to managers
    if created and not hotel.created_by.is_staff:
        mail_managers_task.delay(
                subject='Создан отель #{id}'.format(id=hotel.id),
                template=email_template,
                data=email_data
        )
    if not created and not hotel.modified_by.is_staff:
        mail_managers_task.delay(
                subject='Обновлен отель #{id}'.format(id=hotel.id),
                template=email_template,
                data=email_data
        )


@receiver(post_save, sender=Room, dispatch_uid="hotels_room_post_save")
def hotels_room_post_save(sender, **kwargs):
    """
    Room post save
    :param sender: Tariff
    :param kwargs: dict
    :return:
    """
    room = kwargs['instance']
    created = kwargs['created']
    email_data = {
        'id': room.id,
        'name': room.name,
        'hotel': str(room.property),
        'price': room.price,
    }
    email_template = 'emails/manager_room_save.html'

    # Send emails to managers
    if created and not room.created_by.is_staff:
        mail_managers_task.delay(
                subject='Создана комната #{id}'.format(id=room.id),
                template=email_template,
                data=email_data
        )
    if not created and not room.modified_by.is_staff:
        mail_managers_task.delay(
                subject='Обновлена комната #{id}'.format(id=room.id),
                template=email_template,
                data=email_data
        )
