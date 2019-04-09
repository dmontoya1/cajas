
from django.db import models


class Office(models.Model):
    """Guarda las oficinas en donde el negocio tiene funcionamiento
    """

    number = models.IntegerField(
        'Número de la oficina',
        default=1
    )
    phone_number = models.CharField(
        'Telefono',
        max_length=255,
        blank=True, null=True
    )
    address = models.CharField(
        'Direccion',
        max_length=255,
        blank=True, null=True
    )
    image = models.ImageField(
        'Imágen',
        upload_to='contries/',
        blank=True, null=True
    )

    def __str__(self):
        return "Oficina {}".format(str(self.number))

    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'
        ordering = ['number']
