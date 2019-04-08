from django.contrib.auth import get_user_model

from django.db import models

from office.models.officeCountry import OfficeCountry
from units.models.units import Unit

User = get_user_model()


class SupervisorCalendar(models.Model):
    """
    """

    office = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina',
        related_name='related_supervisor_calendar',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    supervisor = models.ForeignKey(
        User,
        verbose_name='Supervisor',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_supervisor_calendar'
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name='Unidad',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    assigned_date = models.DateField(
        'Fecha de calendario de supervisor',
        auto_now=True,
    )

    def __str__(self):
        return 'calendario'

    class Meta:
        verbose_name = 'Calendario de supervisor'
        verbose_name_plural = 'Calendarios de supervisores'
