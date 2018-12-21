from django.apps import AppConfig


class BoxesConfig(AppConfig):
    name = 'boxes'
    verbose_name = 'Cajas'
    app_label = 'Cajas'

    def ready(self):
        try:
            import boxes.signals  # noqa F401
        except ImportError:
            pass
