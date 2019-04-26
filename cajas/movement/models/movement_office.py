from django.db import models

from boxes.models.box_office import BoxOffice
from .movement_mixin import MovementMixin


class MovementOffice(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de la oficina
    """

    box_office = models.ForeignKey(
        BoxOffice,
        verbose_name='Caja oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de {}".format(self.box_office.office)

    def __init__(self, *args, **kwargs):
        super(MovementOffice, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    class Meta:
        verbose_name = 'Movimiento de la oficina'
        verbose_name_plural = 'Movimientos de la oficina'
