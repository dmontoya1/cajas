from django.apps import AppConfig


class UnitsConfig(AppConfig):
    name = 'units'
    verbose_name = 'Unidades'
    app_label = 'Unidades'

    def ready(self):
        try:
            import units.signals  # noqa F401
        except ImportError:
            pass
