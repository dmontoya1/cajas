from django.db import models

from office.models.office import Office


class OfficeCommitments(models.Model):
    """
    """

    MONTHTLY = 'MO'
    WEEKLY = 'SE'

    PERIOD = (
        (MONTHTLY, 'Mensual'),
        (WEEKLY, 'Semanal')
    )

    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.CASCADE,
        related_name='related_commitments'
    )
    name = models.CharField(
        'Nombre',
        max_length=255
    )
    periodicidad = models.CharField(
        'Periodicidad',
        max_length=2,
        choices=PERIOD,
        blank=True, null=True
    )
    value = models.IntegerField(
        'Valor'
    )
    added_date = models.DateTimeField(
        'Fecha de creacion',
        auto_now_add=True
    )

    def __str__(self):
        return '%s - %s' % (self.name, self.get_periodicidad_display())

    class Meta:
        verbose_name = 'Compromiso Oficina'
        verbose_name_plural = 'Compromisos Oficina'
