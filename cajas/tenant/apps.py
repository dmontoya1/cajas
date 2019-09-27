from django.apps import AppConfig


class TenantConfig(AppConfig):
    name = 'cajas.tenant'
    verbose_name = "Plataformas"

    def ready(self):
        try:
            import tenant.signals  # noqa F401
        except ImportError:
            pass
