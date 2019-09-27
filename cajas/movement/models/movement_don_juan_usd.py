
from django.db import models

from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from .movement_mixin import MovementMixin


class MovementDonJuanUsd(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de Presidente USD
    """

    box_don_juan = models.ForeignKey(
        BoxDonJuanUSD,
        verbose_name='Caja Presidente USD',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )
    movement_don_juan = models.IntegerField(
        "Movimiento Presidente PK",
        blank=True,
        null=True
    )
    movement_office = models.IntegerField(
        "Movimiento Oficina PK",
        blank=True,
        null=True
    )
    movement_box_colombia = models.IntegerField(
        "Movimiento Caja Colombia",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Movimiento de la caja de {} de Presidente".format(self.box_don_juan.office)

    class Meta:
        verbose_name = 'Movimiento de Presidente'
        verbose_name_plural = 'Movimientos de Presidente'
        ordering = ['-date', '-pk']
