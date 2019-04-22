
from django.db import models

from boxes.models.box_daily_square import BoxDailySquare
from boxes.models.box_office import BoxOffice
from boxes.models.box_partner import BoxPartner
from .movement_mixin import MovementMixin


class MovementBetweenOfficeRequest(MovementMixin):
    """
    """

    box_office = models.ForeignKey(
        BoxOffice,
        verbose_name='Caja oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements_between_office'
    )
    observation = models.TextField(
        'Observación',
        help_text='Observación por la cual se debería de aceptar el movimiento'
    )

    def __str__(self):
        return "Transpaso de dinero hacia {}".format(self.box_office.office)

    class Meta:
        verbose_name = 'Requerimiento de Movimiento entre oficinas'
        verbose_name_plural = 'Requerimientos de Movimientos entre oficinas'
