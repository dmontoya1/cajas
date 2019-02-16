from django.apps import AppConfig


class OfficeConfig(AppConfig):
    name = 'office'
    verbose_name = 'Oficinas'
    app_label = 'Oficinas'

    def ready(self):
        try:
            import office.signals  # noqa F401
        except ImportError:
            pass
