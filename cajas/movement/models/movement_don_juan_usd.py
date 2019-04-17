
from django.db import models

from boxes.models.box_don_juan_usd import BoxDonJuanUSD
from .movement_mixin import MovementMixin


class MovementDonJuanUsd(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de don Juan USD
    """

    box_don_juan = models.ForeignKey(
        BoxDonJuanUSD,
        verbose_name='Caja Don Juan USD',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de la caja de {} de Don Juan".format(self.box_don_juan.office)

    def __init__(self, *args, **kwargs):
        super(MovementDonJuanUsd, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    def save(self, *args, **kwargs):
        if self.__movement_type != self.movement_type:
            box = self.box_don_juan
            if self.movement_type == 'IN':
                box.balance = box.balance + (int(self.value) * 2)
            else:
                box.balance = box.balance - (int(self.value) * 2)
            box.save()
        super(MovementDonJuanUsd, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Movimiento de Don Juan'
        verbose_name_plural = 'Movimientos de Don Juan'
