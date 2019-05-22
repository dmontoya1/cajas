from django.db import models

from enumfields import EnumField
from enumfields import Enum

from cajas.users.models.partner import Partner


class BoxStatus(Enum):
    ABIERTA = 'ABIERTA'
    EN_LIQUIDACION = 'ENLIQUID'
    LIQUIDADA = 'LIQUID'

    class Labels:
        ABIERTA = 'Activa'
        EN_LIQUIDACION = 'En Liquidación'
        LIQUIDADA = 'Liquidada'


class BoxPartner(models.Model):
    """Modelo para la caja de un socio
    """

    partner = models.OneToOneField(
        Partner,
        verbose_name='Socio',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='box'
    )
    balance = models.IntegerField(
        "Saldo de la caja",
        default=0
    )
    is_active = models.BooleanField(
        "Caja Activa?",
        default=True
    )
    last_movement_id = models.IntegerField(
        'id último movimiento',
        default=0
    )
    box_status = EnumField(
        BoxStatus,
        verbose_name='Estado de la caja',
        max_length=10,
        default=BoxStatus.ABIERTA
    )

    def __str__(self):
        if self.partner is not None:
            return "Caja de {}".format(self.partner.user.get_full_name())
        return "Caja de usuario eliminado"

    def get_box_status(self):
        return str(self.box_status)

    class Meta:
        verbose_name = 'Caja de socio'
        verbose_name_plural = 'Cajas de socios'
