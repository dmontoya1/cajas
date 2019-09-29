
from django.db import models

from cajas.boxes.models.box_don_juan import BoxDonJuan
from .movement_mixin import MovementMixin


class MovementDonJuan(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de Presidente
    """

    box_don_juan = models.ForeignKey(
        BoxDonJuan,
        verbose_name='Caja Presidente Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )
    movement_box_colombia = models.IntegerField(
        "Movimiento Caja Colombia",
        blank=True,
        null=True
    )
    movement_office = models.IntegerField(
        "Movimiento Oficina PK",
        blank=True,
        null=True
    )
    movement_don_juan_usd = models.IntegerField(
        "Movimiento Presidente Dólares PK",
        null=True,
        blank=True
    )

    def __str__(self):
        if self.box_don_juan.office is not None:
            return "Movimiento de la caja de {} de Presidente".format(self.box_don_juan.office)
        return "Movimiento de la caja de Presidente"

    class Meta:
        verbose_name = 'Movimiento de Presidente'
        verbose_name_plural = 'Movimientos de Presidente'
        ordering = ['-date', '-pk']
