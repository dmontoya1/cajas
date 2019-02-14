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

    def save(self, *args, **kwargs):
        if self.box_partner.balance:
            l_balance = self.box_partner.balance
        else:
            l_balance = 0

        if self.movement_type == MovementPartner.IN:
            self.balance = int(l_balance) + int(self.value)
        else:
            self.balance = int(l_balance) - int(self.value)

        super(MovementPartner, self).save(*args, **kwargs)
        self.box_partner.balance = self.balance
        self.box_partner.last_movement_id = self.pk
        self.box_partner.save()

    class Meta:
        verbose_name = 'Movimiento del socio'
        verbose_name_plural = 'Movimientos del socio'
