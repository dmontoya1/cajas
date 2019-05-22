from django.db import models

from cajas.inventory.models.brand import Brand
from cajas.units.models.units import Unit
from .movement_daily_square import MovementDailySquare


class MovementDailySquareRequestItem(models.Model):
    """
    """

    movement = models.ForeignKey(
        MovementDailySquare,
        verbose_name='Unidad',
        on_delete=models.CASCADE,
        related_name='related_movement_request'
    )
    name = models.CharField(
        'Nombre',
        max_length=255,
        blank=True, null=True
    )
    description = models.TextField(
        'Descripción',
        blank=True, null=True
    )
    price = models.IntegerField(
        'Precio',
        help_text='Precio en la modena local',
        blank=True, null=True
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Marca',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_unit_movement_items'
    )
    is_replacement = models.BooleanField(
        "Item de repuesto?",
        default=False
    )

    def __str__(self):
        return 'movimiento de aprobación para %s' % (self.name)

    class Meta:
        verbose_name = 'Movimiento de Aprobación'
        verbose_name_plural = 'Movimientos de aprobación'
