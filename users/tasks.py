from __future__ import absolute_import
from hh.celery import app
from hh.messangers.mailer import Mailer


@app.task
def mail_managers_task(subject, template, data):
    Mailer.mail_managers(subject=subject, template=template, data=data)
