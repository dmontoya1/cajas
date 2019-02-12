
from django.db import models

from general_config.models.currency import Currency


class Country(models.Model):
    """Guarda los paises en donde el negocio tiene funcionamiento
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
    )
    abbr = models.CharField(
        'Abreviatura',
        max_length=255,
        help_text='MXN, COL, HON, GUA'
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name='Divisa',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        "País Activo?",
        default=True
    )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
