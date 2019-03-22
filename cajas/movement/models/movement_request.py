
from django.db import models

from boxes.models.box_partner import BoxPartner
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

    def __str__(self):
        return "Solicitud de movimiento del {}".format(self.box_partner.partner)

    class Meta:
        verbose_name = 'Requerimiento de Movimiento'
        verbose_name_plural = "Requerimientos de movimientos"
