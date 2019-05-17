from django.db import models


class Category(models.Model):
    """
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
        help_text='Nombre de la categoria. Ejm: Celulares, motos, equipo de oficina, computadores...etc.'
    )
    is_active = models.BooleanField(
        "Categoría Activa?",
        default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorias'
