from django.apps import AppConfig


class ConceptsConfig(AppConfig):
    name = 'cajas.concepts'
    verbose_name = 'Conceptos'
    app_label = 'Conceptos'

    def ready(self):
        try:
            import concepts.signals  # noqa F401
        except ImportError:
            pass
