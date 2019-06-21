from django.db import models

from cajas.office.models.officeCountry import OfficeCountry
from .employee import Employee


class Group(models.Model):
    """Guarda la relacion del Administrador de Grupo con sus supervisores
    """

    admin = models.ForeignKey(
        Employee,
        verbose_name='Administrador de Grupo',
        on_delete=models.CASCADE,
    )
    office = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return "Administrador {}".format(self.admin.user)

    class Meta:
        verbose_name = 'Administrador de grupo'
