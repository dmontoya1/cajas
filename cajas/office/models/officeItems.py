from django.db import models

from inventory.models.brand import Brand
from office.models.office import Office


class OfficeItems(models.Model):
    """
    """

    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.CASCADE,
        related_name='related_items'
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
        related_name='related_office_items'
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

    def __str__(self):
        return '{} de la oficina {}{}'.format(self.name, self.office.country.abbr, self.office.number)

    class Meta:
        verbose_name = 'Inventario oficina'
        verbose_name_plural = 'Inventarios oficinas'
