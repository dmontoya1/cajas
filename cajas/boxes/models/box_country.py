from django.contrib.auth import get_user_model
from django.db import models


from general_config.models.country import Country
from general_config.models.currency import Currency


class BoxCountry(models.Model):
    """Modelo para la caja de un país
    """

    country = models.ForeignKey(
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
    currency = models.ForeignKey(
        Currency,
        verbose_name='Divisa de la caja',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    

    def __str__(self):
        return "Caja de {}".format(self.country.name)


    class Meta:
        unique_together = ("country", "currency")
        verbose_name = 'Caja de País'
        verbose_name_plural = 'Cajas de Paises'
