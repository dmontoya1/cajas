from django.db import models

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.movement.models.movement_mixin import MovementMixin


class MovementBoxColombia(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de la oficina
    """

    box_office = models.ForeignKey(
        BoxColombia,
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
    movement_office = models.IntegerField(
        "Movimiento Oficina PK",
        blank=True,
        null=True
    )
    movement_don_juan_usd = models.IntegerField(
        "Movimiento Don Juan Dólares PK",
        null=True,
        blank=True
    )
    movement_box_colombia = models.IntegerField(
        "Movimiento Caja Colombia PK",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Movimiento de {}".format(self.box_office.office)

    def __init__(self, *args, **kwargs):
        super(MovementBoxColombia, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type

    class Meta:
        verbose_name = 'Movimiento de la caja de Colombia'
        verbose_name_plural = 'Movimientos de la caja de Colombia'
        ordering = ['-date', '-pk']
