
from django.db import models

from cajas.units.models import Unit
from .employee import Employee


class DailySquareUnits(models.Model):
    """
    """

    employee = models.OneToOneField(
        Employee,
        verbose_name='Empleado',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    units = models.ManyToManyField(
        Unit,
        verbose_name='Unidades a cargo',
    )

    def __str__(self):
        return 'Grupo de {}'.format(self.employee)

    class Meta:
        verbose_name = "Ruta a cargo"
        verbose_name_plural = "Rutas a cargo"
