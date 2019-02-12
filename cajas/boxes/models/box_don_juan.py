from django.contrib.auth import get_user_model
from django.db import models

from cajas.users.models.partner import Partner
from office.models.office import Office


class BoxDonJuan(models.Model):
    """Modelo para la cajas de Don Juan Por oficina
    """

    partner = models.ForeignKey(
        Partner,
        verbose_name='Don Juan',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True
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

    def __str__(self):
        try:
            return "Caja de Don Juan de la oficina".format(self.office)
        except:
            return "Caja de don Juan"


    class Meta:
        verbose_name = 'Caja de Don Juan'
        verbose_name_plural = 'Cajas de Don Juan'
