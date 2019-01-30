
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    """ Modelo para guardar las divisas que se van a utilizar en cada pais
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
        help_text='Peso Colombiano, Peso Mexicano, Quetzal'
    )
    abbr = models.CharField(
        'Abreviatura',
        max_length=10,
        help_text='COP, MXN, GTQ'
    )
    is_active = models.BooleanField(
        "Divisa Activa?",
        default=True
    )

    def __str__(self):
        return '%s (%s)' % (self.name, self.abbr)


    class Meta:
        verbose_name = 'Divisa'
        verbose_name_plural = 'Divisas'
