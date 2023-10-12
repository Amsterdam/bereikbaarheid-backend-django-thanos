from django.apps import AppConfig


class BereikbaarheidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bereikbaarheid"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals

