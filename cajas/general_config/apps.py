from django.apps import AppConfig


class GeneralConfigConfig(AppConfig):

    name = 'cajas.general_config'
    verbose_name = 'Configuración general'
    app_label = 'Configuración general'

    def ready(self):
        try:
            import general_config.signals  # noqa F401
        except ImportError:
            pass
