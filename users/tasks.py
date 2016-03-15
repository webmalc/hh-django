from __future__ import absolute_import
from hh.celery import app
from hh.messangers.mailer import Mailer
from users.models import User


@app.task
def mail_managers_task(subject, template, data):
    """
    Mail to site managers
    :param subject: subject string
    :param template: template name
    :param data: data dict for template rendering
    :return: None
    """
    Mailer.mail_managers(subject=subject, template=template, data=data)


@app.task
def mail_user_task(subject, template, data, user_id=None, email=None):
    """
    Mail to site user or email
    :param subject: subject string
    :param template:  subject string
    :param data:  data dict for template rendering
    :param user_id: site user id
    :param email: user email
    :return: boolean
    """
    if email:
        Mailer.mail_user(subject=subject, template=template, data=data, email=email)
        return True

    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            Mailer.mail_user(subject=subject, template=template, data=data, user=user)
            return True
        except User.DoesNotExist:
            return False


