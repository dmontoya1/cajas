from django.contrib.auth import get_user_model
from django.db import models

from boxes.models.box_daily_square import BoxDailySquare
from general_config.models.country import Country
from office.models.office import Office
from units.models.units import Unit
from .movement_mixin import MovementMixin

User = get_user_model()

class MovementDailySquare(MovementMixin):
    """Modelo para guardar los movimientos de las cajas del cuadre diario
    """

    box_daily_square = models.ForeignKey(
        BoxDailySquare,
        verbose_name='Caja Cuadre Diario',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name='Unidad',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    user = models.ForeignKey(
        User,
        verbose_name='Socio, empleado',
        related_name='related_movements',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    country = models.ForeignKey(
        Country,
        verbose_name='País',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return "Movimiento del {}".format(self.box_daily_square.user)


    class Meta:
        verbose_name = 'Movimiento del Cuadre Diario'
        verbose_name_plural = 'Movimientos del Cuadre Diario'
