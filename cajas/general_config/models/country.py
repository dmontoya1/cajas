
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from general_config.models.currency import Currency



class Country(models.Model):
    """Guarda los paises en donde el negocio tiene funcionamiento
    """


    name = models.CharField(
        'Nombre',
        max_length=255,
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name='Divisa',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return '{}'.format(self.name)


    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
