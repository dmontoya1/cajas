from django.apps import AppConfig


class LoansConfig(AppConfig):
    name = 'cajas.loans'
    verbose_name = 'Préstamos'

    def ready(self):
        try:
            import loans.signals  # noqa F401
        except ImportError:
            pass
