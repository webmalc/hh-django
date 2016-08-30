from django.contrib.messages.views import SuccessMessageMixin
from envelope.views import ContactView


class ContactFormView(SuccessMessageMixin, ContactView):
    """
    Contacts form view
    """
    success_message = "Благодарим Вас за отправку письма! Наш специалист ответит Вам в ближайшее время."
