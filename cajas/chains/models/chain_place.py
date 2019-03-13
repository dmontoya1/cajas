
from django.db import models

from .chain import Chain


class ChainPlace(models.Model):
    """

    """

    chain = models.ForeignKey(
        Chain,
        verbose_name='Cadena',
        on_delete=models.CASCADE,
        related_name='related_places'
    )
    pay_date = models.DateField(
        'Fecha de pago del puesto',
        auto_now=False,
    )

    def __str__(self):
        return "Puesto de la cadena {}".format(self.chain)

    class Meta:
        verbose_name = "Puesto de la cadena"
        verbose_name_plural = "Puestos de la cadena"
