from django.apps import AppConfig


class TenantConfig(AppConfig):
    name = 'cajas.tenant'

    def ready(self):
        try:
            import tenant.signals  # noqa F401
        except ImportError:
            pass
