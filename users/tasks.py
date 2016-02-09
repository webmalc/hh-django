from __future__ import absolute_import
from hh.celery import app
from hh.messangers.mailer import Mailer
from users.models import User


@app.task
def mail_managers_task(subject, template, data):
    Mailer.mail_managers(subject=subject, template=template, data=data)


@app.task
def mail_user_task(subject, template, data, user_id):
    try:
        user = User.objects.get(pk=user_id)
        Mailer.mail_user(subject=subject, template=template, data=data, user=user)
    except User.DoesNotExist:
        pass

