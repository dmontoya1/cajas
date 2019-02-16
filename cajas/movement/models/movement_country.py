from django.db import models

from boxes.models.box_country import BoxCountry
from .movement_mixin import MovementMixin


class MovementCountry(MovementMixin):
    """Modelo para guardar los movimientos de las cajas del país
    """

    box_country = models.ForeignKey(
        BoxCountry,
        verbose_name='Caja País',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de {}".format(self.box_country.country)

    class Meta:
        verbose_name = 'Movimiento del país'
        verbose_name_plural = 'Movimientos del país'
