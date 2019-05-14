from django.db import models

from cajas.boxes.models.box_provisioning import BoxProvisioning
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

    def __init__(self, *args, **kwargs):
        super(MovementProvisioning, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    def save(self, *args, **kwargs):
        if self.__movement_type != self.movement_type:
            box = self.box_daily_square
            if self.movement_type == 'IN':
                box.balance = box.balance + (int(self.value) * 2)
            else:
                box.balance = box.balance - (int(self.value) * 2)
            box.save()
        super(MovementProvisioning, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Movimiento de aprovisionamiento'
        verbose_name_plural = 'Movimientos de aprovisionamiento'
