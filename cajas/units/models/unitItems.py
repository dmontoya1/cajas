from django.db import models

from cajas.inventory.models.brand import Brand
from ..models.units import Unit
from cajas.office.models.officeCountry import OfficeCountry


class UnitItems(models.Model):
    """
    """

    unit = models.ForeignKey(
        Unit,
        verbose_name='Unidad',
        on_delete=models.CASCADE,
        related_name='related_items',
        blank=True, null=True
    )
    office = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina por país',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    name = models.CharField(
        'Nombre',
        max_length=255
    )
    description = models.TextField(
        'Descripción',
        blank=True, null=True
    )
    price = models.IntegerField(
        'Precio',
        help_text='Precio en la modena local'
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name='Marca',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_unit_items'
    )
    is_deleted = models.BooleanField(
        'Item Eliminado?',
        default=False
    )
    observations = models.TextField(
        'Observaciones',
        help_text='Por que se elimino el item?',
        blank=True, null=True
    )
    is_replacement = models.BooleanField(
        "Item de repuesto?",
        default=False
    )

    def __str__(self):
        return  self.name #' de la unidad ' # % (self.name, self.unit.name)

    class Meta:
        verbose_name = 'Inventario unidad'
        verbose_name_plural = 'Inventarios unidades'
