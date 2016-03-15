from django.apps import AppConfig


class BookingAppConfig(AppConfig):
    name = 'booking'

    def ready(self):
        import booking.signals
