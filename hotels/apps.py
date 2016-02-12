from django.apps import AppConfig


class HotelsAppConfig(AppConfig):
    name = 'hotels'

    def ready(self):
        import hotels.signals