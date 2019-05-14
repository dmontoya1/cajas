from django.apps import AppConfig


class MovementConfig(AppConfig):
    name = 'cajas.movement'
    verbose_name = 'Movimientos'

    def ready(self):
        try:
            import cajas.movement.signals  # noqa F401
        except ImportError:
            pass
