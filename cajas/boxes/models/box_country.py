from django.contrib.auth import get_user_model
from django.db import models

from general_config.models.country import Country


class BoxCountry(models.Model):
    """Modelo para la caja de un país
    """

    country = models.OneToOneField(
        Country,
        verbose_name='País',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    balance = models.IntegerField(
        "Saldo de la caja",
        default=0
    )
    is_active = models.BooleanField(
        "Caja Activa?",
        default=True
    )

    def __str__(self):
        return "Caja de {}".format(self.country.name)


    class Meta:
        verbose_name = 'Caja de País'
        verbose_name_plural = 'Cajas de Paises'
