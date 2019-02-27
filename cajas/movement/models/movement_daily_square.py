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

    APPROVED = 'AP'
    DENIED = 'DE'
    DISPERSED = 'DI'

    STATUS = (
        (APPROVED, 'Aprobado'),
        (DENIED, 'Rechazado'),
        (DISPERSED, 'Dispersado')
    )

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
    review = models.BooleanField(
        'Movimiento Revisado?',
        default=False
    )
    status = models.CharField(
        'Estado de la revisión',
        max_length=2,
        choices=STATUS,
        blank=True,
        null=True,
    )
    denied_detail = models.TextField(
        'Detalle del rechazo del movimiento',
        blank=True,
        null=True
    )

    # def save(self, *args, **kwargs):
    #     if self.box_daily_square.balance:
    #         l_balance = self.box_daily_square.balance
    #     else:
    #         l_balance = 0

    #     if self.movement_type == MovementDailySquare.IN:
    #         self.balance = int(l_balance) + int(self.value)
    #     else:
    #         self.balance = int(l_balance) - int(self.value)

    #     super(MovementDailySquare, self).save(*args, **kwargs)
    #     self.box_daily_square.balance = self.balance
    #     self.box_daily_square.last_movement_id = self.pk
    #     self.box_daily_square.save()

    def __str__(self):
        return "Movimiento de {}".format(self.box_daily_square.user)

    class Meta:
        verbose_name = 'Movimiento del Cuadre Diario'
        verbose_name_plural = 'Movimientos del Cuadre Diario'
