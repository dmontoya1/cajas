
from django.db import models

from enumfields import EnumField
from enumfields import Enum


class ConceptType(Enum):
    SIMPLE = 'SM'
    DOUBLE = 'DB'
    SIMPLEDOUBLE = 'SD'

    class Labels:
        SIMPLE = 'Simple'
        DOUBLE = 'Doble'
        SIMPLEDOUBLE = 'Simple y doble'


class CrossoverType(Enum):
    PARTNER = 'PA'
    OFFICE = 'OF'

    class Labels:
        PARTNER = 'Socio directo'
        OFFICE = 'Oficina'


class Relationship(Enum):
    UNIT = 'UNIT'
    PERSON = 'PERS'
    COUNTRY = 'COUNTRY'
    LOAN = 'PREST'
    CHAIN = 'CHAIN'

    class Labels:
        UNIT = 'Unidad'
        PERSON = 'Persona'
        COUNTRY = 'País'
        LOAN = 'Préstamo'
        CHAIN = 'Cadena'


class Concept(models.Model):
    """
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
    )
    description = models.TextField(
        'Descripción'
    )
    concept_type = EnumField(
        ConceptType,
        verbose_name='Tipo de concepto',
        max_length=2,
    )
    crossover_type = EnumField(
        CrossoverType,
        verbose_name='Tipo de cruce',
        max_length=2,
        blank=True, null=True
    )
    counterpart = models.ForeignKey(
        'self',
        verbose_name='Concepto Contrapartida',
        help_text='Concepto de contrapartida cuando el concepto es de cruce.',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    relationship = EnumField(
        Relationship,
        max_length=7,
        verbose_name='Relación del movimiento',
        blank=True, null=True
    )
    movement_type = models.BooleanField(
        'El concepto genera movimiento en la caja?',
        default=True,
        help_text='Indicar si el movimiento genera o no un movimiento en las cajas. Como el caso de ENTREGA DE DINERO. Éste no génera movimiento en la caja'
    )
    is_active = models.BooleanField(
        'Concepto activo?',
        default=True
    )

    def __str__(self):
        return 'Concepto %s de tipo %s' % (self.name, self.get_concept_type_display())

    class Meta:
        verbose_name = 'Concepto'
