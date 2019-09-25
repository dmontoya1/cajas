from django.db import models

from cajas.boxes.models.box_office import BoxOffice
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
    movement_don_juan = models.IntegerField(
        "Movimiento Don Juan PK",
        blank=True,
        null=True
    )
    movement_box_colombia = models.IntegerField(
        "Movimiento Oficina Colombia PK",
        blank=True,
        null=True
    )
    movement_don_juan_usd = models.IntegerField(
        "Movimiento Don Juan Dólares PK",
        null=True,
        blank=True
    )

    def __str__(self):
        if self.box_office:
            return "Movimiento de {}".format(self.box_office.office)
        return "Movimiento de oficina"

    def __init__(self, *args, **kwargs):
        super(MovementOffice, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    class Meta:
        verbose_name = 'Movimiento de la oficina'
        verbose_name_plural = 'Movimientos de la oficina'
        ordering = ['-date', '-pk']
