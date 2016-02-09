from django.core.mail import mail_managers, send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Mailer:
    @staticmethod
    def mail_managers(subject, template, data):
        mail_managers(subject=subject, message='', html_message=render_to_string(template, data))

    @staticmethod
    def mail_user(subject, template, data, user):
        send_mail(
            recipient_list=user.get_emails(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject='{prefix} {text}'.format(prefix=settings.EMAIL_SUBJECT_PREFIX, text=subject),
            message='',
            html_message=render_to_string(template, data)
        )
