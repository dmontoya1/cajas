from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

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
        return '%s de la oficina %s' % (self.name, self.office.name)


    class Meta:
        verbose_name = 'Inventario oficina'
        verbose_name_plural = 'Inventarios oficinas'

