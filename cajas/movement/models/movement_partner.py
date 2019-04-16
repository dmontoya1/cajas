from django.db import models

from boxes.models.box_partner import BoxPartner
from .movement_mixin import MovementMixin


class MovementPartner(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de un socio
    """

    box_partner = models.ForeignKey(
        BoxPartner,
        verbose_name='Caja Socio',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento del {}".format(self.box_partner.partner)


    class Meta:
        verbose_name = 'Movimiento del socio'
        verbose_name_plural = 'Movimientos del socio'
