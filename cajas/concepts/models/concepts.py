
from django.contrib.auth import get_user_model
from django.db import models


class Concept(models.Model):
    """
    """

    SIMPLE = 'SM'
    DOUBLE = 'DB'
    SIMPLEDOUBLE = 'SD'
    
    PARTNER = 'PA'
    OFFICE = 'OF'

    UNIT = 'UNIT'
    PERSON = 'PERS'
    COUNTRY = 'COUNTRY'
    LOAN = 'PREST'
    CHAIN = 'CHAIN'

    TYPES_CONCEPT = (
        (SIMPLE, 'Simple'),
        (DOUBLE, 'Doble partida'),
        (SIMPLEDOUBLE, 'Simple y Doble Partida')
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
    counterpart = models.ForeignKey(
        'self',
        verbose_name='Concepto Contrapartida',
        help_text='Concepto de contrapartida cuando el concepto es de cruce.',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    relationship = models.CharField(
        'Relacion del movimiento',
        max_length=10,
        choices=RELATIONSHIPS,
        blank=True, null=True
    )
    movement_type = models.BooleanField(
        'El concepto genera movimiento en la caja?',
        default = True,
        help_text = 'Indicar si el movimiento genera o no un movimiento en las cajas. Como el caso de ENTREGA DE DINERO. Éste no génera movimiento en la caja'
    )
    is_active = models.BooleanField(
        'Concepto activo?',
        default=True
    )

    def __str__(self):
        return 'Concepto %s de tipo %s' % (self.name, self.get_concept_type_display())

    
    class Meta:
        verbose_name = 'Concepto'
