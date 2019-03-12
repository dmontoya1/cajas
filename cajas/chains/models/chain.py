from django.db import models

from office.models.office import Office


class Chain(models.Model):
    """

    """
    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        related_name='related_chaines',
        on_delete=models.CASCADE,
        null=True
    )
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
