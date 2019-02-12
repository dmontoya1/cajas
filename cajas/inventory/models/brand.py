from django.db import models

from inventory.models.category import Category


class Brand(models.Model):
    """
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
        help_text='Nombre de la marca. Ejm: Samsung, Honda, HP, ... etc.'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Categoria',
        on_delete=models.CASCADE,
        related_name='related_brands'
    )
    is_active = models.BooleanField(
        "Marca Activa?",
        default=True
    )

    def __str__(self):
        return '%s (%s)' % (self.name, self.category.name)

    class Meta:
        verbose_name = 'Marca'
