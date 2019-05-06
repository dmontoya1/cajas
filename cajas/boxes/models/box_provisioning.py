from django.db import models

from cajas.office.models.officeCountry import OfficeCountry


class BoxProvisioning(models.Model):
    """Modelo para la caja de la oficina de un aprovisionamiento
    """

    office = models.OneToOneField(
        OfficeCountry,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='box_provisioning'
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
            return "Caja de {}".format(self.office)
        return "Caja de aprovisionamiento"

    class Meta:
        verbose_name = 'Caja de aprovisionamiento'
        verbose_name_plural = 'Cajas de aprovisionamientos'
