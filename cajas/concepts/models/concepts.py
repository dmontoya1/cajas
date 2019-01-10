
from django.contrib.auth import get_user_model
from django.db import models


class Concept(models.Model):
    """
    """

    SIMPLE = 'SM'
    DOUBLE = 'DB'
    
    PARTNER = 'PA'
    OFFICE = 'OF'

    UNIT = 'UNIT'
    PERSON = 'PERS'
    COUNTRY = 'COUNTRY'
    LOAN = 'PREST'
    CHAIN = 'CHAIN'

    TYPES_CONCEPT = (
        (SIMPLE, 'Simple'),
        (DOUBLE, 'Doble partida')
    )

    CROSSOVER = (
        (PARTNER, 'Socio Directo'),
        (OFFICE, 'Oficina')
    )

    RELATIONSHIPS = (
        (UNIT, 'Unidad'),
        (PERSON, 'Socio, empleado'),
        (COUNTRY, 'Pais'),
        (LOAN, 'Prestamo'),
        (CHAIN, 'Cadena'),
        (OFFICE, 'Oficina')
    )



    name = models.CharField(
        'Nombre',
        max_length=255,
    )
    description = models.TextField(
        'Descripción'
    )
    concept_type = models.CharField(
        'Tipo de concepto',
        max_length=5,
        choices=TYPES_CONCEPT
    )
    crossover_type = models.CharField(
        'Tipo de Cruce',
        max_length=5,
        choices=CROSSOVER,
        blank=True, null=True
    )
    counterpart_name = models.CharField(
        'Nombre Contrapartida',
        max_length=255,
        help_text='Nombre de la contrapartida cuando el concepto es de cruce. Ejm. Venta--> Compra. '
    )
    relationship = models.CharField(
        'Relacion del movimiento',
        max_length=10,
        choices=RELATIONSHIPS,
        blank=True, null=True
    )
    # unit = models.ForeignKey(
    #     Unit,
    #     verbose_name='Unidad',
    #     on_delete=models.SET_NULL,
    #     blank=True, null=True
    # )
    # user = models.ForeignKey(
    #     User,
    #     'Socio, empleado',
    #     on_delete=models.SET_NULL,
    #     blank=True, null=True
    # )


    def __str__(self):
        return 'Concepto %s de tipo %s' % (self.name, self.get_concept_type_display())

    
    class Meta:
        verbose_name = 'Concepto'
