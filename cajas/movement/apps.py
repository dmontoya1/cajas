from django.apps import AppConfig


class MovementConfig(AppConfig):
    name = 'movement'
    verbose_name = 'Movements'

    def ready(self):
        try:
            import movement.signals  # noqa F401
        except ImportError:
            pass
