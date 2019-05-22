from django.contrib.auth import get_user_model
from django.db import models

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.movement.models.movement_don_juan import MovementDonJuan
from cajas.movement.models.movement_don_juan_usd import MovementDonJuanUsd
from cajas.movement.models.movement_office import MovementOffice
from cajas.movement.models.movement_partner import MovementPartner
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
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
    movement_don_juan = models.OneToOneField(
        MovementDonJuan,
        verbose_name='Movimiento Don Juan Contrapartida',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    movement_don_juan_usd = models.OneToOneField(
        MovementDonJuanUsd,
        verbose_name='Movimiento Don Juan Dolares Contrapartida',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    movement_partner = models.OneToOneField(
        MovementPartner,
        verbose_name='Movimiento Socio Contrapartida',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    movement_office = models.OneToOneField(
        MovementOffice,
        verbose_name='Movimiento Oficina Contrapartida',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    movement_cd = models.OneToOneField(
        "self",
        verbose_name='Movimiento CD Contrapartida',
        on_delete=models.SET_NULL,
        null=True, blank=True
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
    office = models.ForeignKey(
        OfficeCountry,
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

    def __str__(self):
        return "Movimiento de {}".format(self.box_daily_square.user)

    def __init__(self, *args, **kwargs):
        super(MovementDailySquare, self).__init__(*args, **kwargs)
        self.__movement_type = self.movement_type
        self.__value = self.value

    def save(self, *args, **kwargs):
        if self.__movement_type != self.movement_type:
            box = self.box_daily_square
            if self.movement_type == 'IN':
                box.balance = box.balance + (int(self.value) * 2)
            else:
                box.balance = box.balance - (int(self.value) * 2)
            box.save()
        if self.__value != self.value:
            box = self.box_daily_square
            if self.movement_type == 'IN':
                box.balance -= int(self.value)
                box.balance += int(self.value)
            else:
                box.balance += int(self.value)
                box.balance -= int(self.value)
            box.save()
        super(MovementDailySquare, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Movimiento del Cuadre Diario'
        verbose_name_plural = 'Movimientos del Cuadre Diario'
