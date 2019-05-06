from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'cajas.inventory'
    verbose_name = 'Inventario'
    app_label = 'Inventario'

    def ready(self):
        try:
            import inventory.signals  # noqa F401
        except ImportError:
            pass
