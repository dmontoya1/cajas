from django.db import models

from office.models.officeCountry import OfficeCountry


class Chain(models.Model):
    """
    """

    INTERNA = 'IN'
    EXTERNA = 'EX'

    CHAIN_TYPE = (
        (INTERNA, 'Interna'),
        (EXTERNA, 'Externa'),
    )

    office = models.ForeignKey(
        OfficeCountry,
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
    chain_type = models.CharField(
        'Tipo de cadena',
        max_length=2,
        choices=CHAIN_TYPE,
        default=INTERNA
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cadena"
