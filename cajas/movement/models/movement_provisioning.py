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

    def save(self, *args, **kwargs):
        if self.box_provisioning.balance:
            l_balance = self.box_provisioning.balance
        else:
            l_balance = 0

        if self.movement_type == MovementProvisioning.IN:
            self.balance = int(l_balance) + int(self.value)
        else:
            self.balance = int(l_balance) - int(self.value)

        super(MovementProvisioning, self).save(*args, **kwargs)
        self.box_provisioning.balance = self.balance
        self.box_provisioning.last_movement_id = self.pk
        self.box_provisioning.save()

    class Meta:
        verbose_name = 'Movimiento de aprovisionamiento'
        verbose_name_plural = 'Movimientos de aprovisionamiento'
