
from django.db import models

from concepts.models.concepts import Concept
from office.models.office import Office


class Notifications(models.Model):
    """
    """

    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        related_name='related_supervisor_calendar',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    concept = models.ForeignKey(
        Concept,
        verbose_name='Concepto',
        on_delete=models.CASCADE,
    )
    detail = models.TextField(
        'Detalle del pago',
        default=''
    )
    value = models.FloatField(
        'Valor del pago'
    )

    def __str__(self):
        return 'Notification {}'.format(self.office)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notificationes'
