from django.db import models

from cajas.users.models.partner import Partner
from cajas.office.models.officeCountry import OfficeCountry


class BoxDonJuan(models.Model):
    """Modelo para la cajas del Presidente Por oficina
    """

    partner = models.ForeignKey(
        Partner,
        verbose_name='Presidente',
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
            return "Caja del Presidente {}".format(self.office)
        return "Caja del Presidente"

    class Meta:
        verbose_name = 'Caja del Presidente'
        verbose_name_plural = 'Cajas del Presidente'
