
from django.db import models

from cajas.boxes.models.box_partner import BoxPartner
from .movement_mixin import MovementMixin


class MovementRequest(MovementMixin):
    """
    """

    box_partner = models.ForeignKey(
        BoxPartner,
        verbose_name='Caja Socio',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_request'
    )
    observation = models.TextField(
        'Observación',
        help_text='Observación por la cual se debería de aceptar el movimiento que sobrepasó el tope'
    )
    withdraw_reason = models.TextField(
        'Razón de solicitud de permiso retiro de socio',
        blank=True, null=True
    )

    def __str__(self):
        if self.box_partner:
            return "Solicitud de movimiento del {}".format(self.box_partner.partner)
        return "Solicitud"

    def __init__(self, *args, **kwargs):
        super(MovementRequest, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    def save(self, *args, **kwargs):
        if self.__movement_type != self.movement_type:
            box = self.box_partner
            if self.movement_type == 'IN':
                box.balance = box.balance + (int(self.value) * 2)
            else:
                box.balance = box.balance - (int(self.value) * 2)
            box.save()
        super(MovementRequest, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Requerimiento de Movimiento'
        verbose_name_plural = "Requerimientos de movimientos"
