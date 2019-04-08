from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from enumfields import EnumField
from enumfields import Enum

from office.models.officeCountry import OfficeCountry

User = get_user_model()


class LoanType(Enum):
    SOCIO_DIRECTO = 'DIR'
    EMPLEADO = 'EMP'
    TERCERO = 'TER'

    class Labels:
        SOCIO_DIRECTO = 'Socio Directo'
        EMPLEADO = 'Empleado'
        TERCERO = 'Tercero'


class Loan(models.Model):
    """
    """

    provider = models.ForeignKey(
        User,
        verbose_name='Fondeador',
        on_delete=models.CASCADE,
        related_name='related_provider_loan',
        null=True, blank=True
    )
    lender = models.ForeignKey(
        User,
        verbose_name='Deudor',
        on_delete=models.CASCADE,
        related_name='related_lender_user'
    )
    office = models.ForeignKey(
        OfficeCountry,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        null=True
    )
    loan_type = EnumField(
        LoanType,
        verbose_name='Tipo de préstamo',
        max_length=3,
    )
    value = models.FloatField(
        'Valor del préstamo (Divisa local)',
    )
    value_cop = models.FloatField(
        'Valor del préstamo (En COP)'
    )
    interest = models.FloatField(
        'Porcentaje de interés'
    )
    time = models.IntegerField(
        'Plazo (en meses)',
        blank=True,
        null=True
    )
    balance = models.FloatField(
        'Saldo a la fecha'
    )
    exchange = models.FloatField(
        'Tasa de cambio',
        default=0
    )
    description = models.TextField(
        'Descripción del Préstamo (terceros)',
        blank=True,
        null=True
    )

    def __str__(self):
        if self.provider:
            return "Préstamo de {} a {} por valor de {}".format(
                self.provider.get_full_name(),
                self.lender.get_full_name(),
                self.value
            )
        return "Préstamo de la oficina a {} por valor de {}".format(
            self.lender.get_full_name(),
            self.value
        )

    def save(self, *args, **kwargs):
        if self.pk:
            loans = self.related_payments.all().aggregate(Sum('value'))
            self.balance = self.value - loans['value__sum']
        else:
            self.balance = self.value
        super(Loan, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Préstamo'
