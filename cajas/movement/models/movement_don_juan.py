from django.db import models

from boxes.models.box_don_juan import BoxDonJuan
from .movement_mixin import MovementMixin


class MovementDonJuan(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de don Juan
    """

    box_don_juan = models.ForeignKey(
        BoxDonJuan,
        verbose_name='Caja Don Juan Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de la caja de {} de Don Juan".format(self.box_don_juan.office)

    def save(self, *args, **kwargs):
        if self.box_don_juan.balance:
            l_balance = self.box_don_juan.balance
        else:
            l_balance = 0

        if self.movement_type == MovementDonJuan.IN:
            self.balance = int(l_balance) + int(self.value)
        else:
            self.balance = int(l_balance) - int(self.value)

        super(MovementDonJuan, self).save(*args, **kwargs)
        self.box_don_juan.balance = self.balance
        self.box_don_juan.last_movement_id = self.pk
        self.box_don_juan.save()

    class Meta:
        verbose_name = 'Movimiento de Don Juan'
        verbose_name_plural = 'Movimientos de Don Juan'
