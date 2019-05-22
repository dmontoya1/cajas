
from django.db import models

from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry


class Notifications(models.Model):
    """
    """
    office = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina Destinatario',
        related_name='related_office_movement',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    office_sender = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina Remitente',
        related_name='related_office_sender_movement',
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
