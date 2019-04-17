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

    def __init__(self, *args, **kwargs):
        super(MovementPartner, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    def save(self, *args, **kwargs):
        if self.__movement_type != self.movement_type:
            box = self.box_partner
            if self.movement_type == 'IN':
                box.balance = box.balance + (int(self.value) * 2)
            else:
                box.balance = box.balance - (int(self.value) * 2)
            box.save()
        super(MovementPartner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Movimiento del socio'
        verbose_name_plural = 'Movimientos del socio'
