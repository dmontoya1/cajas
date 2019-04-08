from django.db import models

from cajas.users.models.partner import Partner
from office.models.officeCountry import OfficeCountry


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
        OfficeCountry,
        verbose_name='Oficina por país',
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
        if self.office is not None:
            return "Caja de Don Juan de la oficina".format(self.office)
        return "Caja de don Juan"

    class Meta:
        verbose_name = 'Caja de Don Juan'
        verbose_name_plural = 'Cajas de Don Juan'
