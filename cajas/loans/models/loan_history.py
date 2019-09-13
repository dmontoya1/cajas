
from datetime import datetime

from django.db import models

from cajas.general_config.models.exchange import Exchange
from cajas.webclient.views.utils import get_object_or_none

from .loan import Loan


class LoanHistory(models.Model):
    """
    """

    LOAN = 'LO'
    INTEREST = 'IN'
    ABONO = 'AB'

    IN = 'IN'
    OUT = 'OUT'

    MOVEMENT_TYPE = (
        (IN, 'Entra'),
        (OUT, 'Sale')
    )

    HISTORY_TYPE = (
        (LOAN, 'Préstamo'),
        (INTEREST, 'Interés'),
        (ABONO, 'Abono')
    )
    loan = models.ForeignKey(
        Loan,
        verbose_name='Préstamo',
        on_delete=models.CASCADE,
        related_name='related_payments'
    )
    history_type = models.CharField(
        'Tipo de historial',
        max_length=2,
        choices=HISTORY_TYPE,
        null=True
    )
    movement_type = models.CharField(
        'Tipo de movimiento',
        max_length=10,
        choices=MOVEMENT_TYPE,
        null=True
    )
    value = models.FloatField(
        'Valor'
    )
    value_cop = models.FloatField(
        'Valor en COP',
        default=0
    )
    date = models.DateField(
        'Fecha del pago',

    )
    balance = models.FloatField(
        'Saldo a la Fecha',
        default=0
    )
    balance_cop = models.FloatField(
        'Saldo a la Fecha (COP)',
        default=0
    )

    def __str__(self):
        if self.history_type:
            return "{} de {}".format(self.get_history_type_display(), self.loan)
        return "Pago de {}".format(self.loan)

    def save(self, *args, **kwargs):
        loan = self.loan
        office = self.loan.office
        exchange = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=datetime.now().month,
        )
        if self.history_type == self.ABONO:
            loan.balance_cop -= float(self.value_cop)
            loan.balance = loan.balance_cop / exchange.exchange_cop_abono
        elif self.history_type == self.LOAN:
            loan.balance += float(self.value)
            loan.balance_cop += float(self.value_cop)
        loan.save()
        super(LoanHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Historial de préstamo'
        verbose_name_plural = 'Historial de préstamos'
        ordering = ['date', 'pk']
