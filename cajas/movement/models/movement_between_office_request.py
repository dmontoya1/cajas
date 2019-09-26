
from django.db import models

from .movement_mixin import MovementMixin


class MovementBetweenOfficeRequest(MovementMixin):
    """
    """

    BOX_DON_JUAN = "BDJ"
    BOX_COLOMBIA = 'BCO'

    FROM_BOX_TYPE = (
        (BOX_DON_JUAN, 'Caja de Presidente'),
        (BOX_COLOMBIA, 'Caja Colombia')
    )

    box_office = models.ForeignKey(
        'boxes.BoxOffice',
        verbose_name='Caja oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements_between_office'
    )
    origin_office = models.ForeignKey(
        'boxes.BoxOffice',
        verbose_name='Caja oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements_between_office_origin'
    )
    from_box_type = models.CharField(
        'Origen del movimiento',
        max_length=3,
        default=BOX_DON_JUAN,
        choices=FROM_BOX_TYPE
    )
    origin_movement_pk = models.IntegerField(
        'PK movimiento origen',
        null=True, blank=True
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
        ordering = ['-date', '-pk']
