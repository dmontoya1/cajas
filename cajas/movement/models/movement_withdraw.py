
from django.db import models

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.boxes.models.box_partner import BoxPartner
from .movement_mixin import MovementMixin


class MovementWithdraw(MovementMixin):
    """
    """

    box_daily_square = models.ForeignKey(
        BoxDailySquare,
        verbose_name='Caja Cuadre Diario',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_withdraw'
    )
    box_partner = models.ForeignKey(
        BoxPartner,
        verbose_name='Caja Socio',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_withdraw'
    )
    observation = models.TextField(
        'Observación',
        help_text='Observación por la cual se debería de aceptar el movimiento'
    )
    withdraw_reason = models.TextField(
        'Razón de solicitud de permiso retiro de socio',
        blank=True, null=True
    )

    def __str__(self):
        return "Solicitud de retiro del {}".format(self.box_partner.partner)

    class Meta:
        verbose_name = 'Requerimiento de retiro'
        verbose_name_plural = "Requerimientos de retiro"
        ordering = ['date', ]
