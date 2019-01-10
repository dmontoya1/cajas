from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    """
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
        help_text='Nombre de la categoria. Ejm: Celulares, motos, equipo de oficina, computadores...etc.'
    )


    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorias'
