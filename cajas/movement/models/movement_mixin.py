from django.contrib.auth import get_user_model
from django.db import models

from cajas.concepts.models.concepts import Concept

User = get_user_model()


def get_sentinel_concept():
    return Concept.objects.get(name='Préstamo empleado')


class MovementMixin(models.Model):
    """Modelo base para todos los movimientos de las cajas y
    cuadre diario
    """

    IN = 'IN'
    OUT = 'OUT'

    MOVEMENT_TYPE = (
        (IN, 'Entra'),
        (OUT, 'Sale')
    )
    concept = models.ForeignKey(
        Concept,
        verbose_name='Concepto',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    movement_type = models.CharField(
        'Tipo de movimiento',
        max_length=10,
        choices=MOVEMENT_TYPE
    )
    value = models.IntegerField(
        'Valor',
        default=0
    )
    detail = models.TextField(
        'Detalle',
        blank=True, null=True
    )
    date = models.DateField(
        'Fecha',
        auto_now_add=False
    )
    responsible = models.ForeignKey(
        User,
        verbose_name='Responsable',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    ip = models.GenericIPAddressField(
        "Dirección IP responsable",
        protocol='both',
        blank=True, null=True
    )
    balance = models.IntegerField(
        'Saldo a la fecha',
        default=0
    )

    class Meta:
        abstract = True
