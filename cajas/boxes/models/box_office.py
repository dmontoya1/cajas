from django.db import models

from office.models.officeCountry import OfficeCountry


class BoxOffice(models.Model):
    """Modelo para la caja de la oficina de un país
    """

    office = models.OneToOneField(
        OfficeCountry,
        verbose_name='Oficina del País',
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

    def __str__(self):
        if self.name and self.office:
            return "Caja {} de {}".format(self.name, self.office)
        if self.office:
            return "Caja de {}".format(self.office)
        return "Caja de oficina"

    class Meta:
        verbose_name = 'Caja de oficinas'
        verbose_name_plural = 'Cajas de Oficina'
