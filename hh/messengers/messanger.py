from django.template.loader import render_to_string
from users.models import UserMessage


class Messenger:

    @staticmethod
    def add_message(user, text=None, template=None, data=[], icon=None):
        message = UserMessage()
        message.user = user
        content = None
        if text:
            content = text
        if template:
            content = render_to_string(template, data)
        if not content:
            raise AttributeError('Content is not defined')
        message.content = content

        if icon:
            message.icon = icon
        message.save()

    @staticmethod
    def get_messages(user, message_type=None, delete=True):
        q = UserMessage.objects.filter(user=user)
        if message_type:
            q = q.filter(type=message_type)
        messages = list(q.values())
        if delete:
            q.delete()

        return messages

