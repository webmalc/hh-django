from django.apps import AppConfig


class PaymentsAppConfig(AppConfig):
    name = 'payments'

    def ready(self):
        import payments.signals
