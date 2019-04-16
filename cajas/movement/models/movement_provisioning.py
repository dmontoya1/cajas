from django.db import models

from boxes.models.box_provisioning import BoxProvisioning
from .movement_mixin import MovementMixin


class MovementProvisioning(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de la oficina
    """

    box_provisioning = models.ForeignKey(
        BoxProvisioning,
        verbose_name='Caja aprovisionamiento',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de {}".format(self.box_provisioning.office)

    class Meta:
        verbose_name = 'Movimiento de aprovisionamiento'
        verbose_name_plural = 'Movimientos de aprovisionamiento'
