from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

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


    def __str__(self):
        return '%s (%s)' % (self.name, self.category.name)


    class Meta:
        verbose_name = 'Marca'
