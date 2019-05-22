from django.apps import AppConfig


class ChainsConfig(AppConfig):
    name = 'cajas.chains'
    verbose_name = 'Cadenas'

    def ready(self):
        try:
            import chains.signals  # noqa F401
        except ImportError:
            pass
