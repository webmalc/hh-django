from django.template.loader import render_to_string
from users.models import UserMessage


class Messenger:

    @staticmethod
    def add_message(user, subject=None, text=None, template=None, data={}, icon=None, message_type=None):
        message = UserMessage()
        message.user = user
        message.subject = subject
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
        if message_type:
            message.type = message_type
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

