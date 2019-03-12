from django.db import models


class Chain(models.Model):
    """

    """
    name = models.CharField(
        'Nombre Cadena',
        max_length=255,
    )
    places = models.IntegerField(
        'Número de puestos',
        default=1
    )
    place_value = models.FloatField(
        'Precio por puesto',
        default=0
    )
    external_chain = models.BooleanField(
        'Es una cadena externa?',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cadena"
