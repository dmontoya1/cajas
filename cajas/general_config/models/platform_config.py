
from django.db import models


class PlatformConfig(models.Model):
    """ Modelo para guardar la configuración de la plataforma, como el nombre del presidente-
    """

    def __str__(self):
        return ''

    class Meta:
        verbose_name = 'Tasa de cambio'
        verbose_name_plural = 'Tasas de cambio'
