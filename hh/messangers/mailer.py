from django.core.mail import mail_managers
from django.template.loader import render_to_string


class Mailer:

    @staticmethod
    def mail_managers(subject, template, data):
        mail_managers(subject=subject, message='', html_message=render_to_string(template, data))
