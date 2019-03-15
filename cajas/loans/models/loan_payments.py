
from django.db import models
from django.db.models import Sum

from .loan import Loan


class LoanPayment(models.Model):
    """
    """

    loan = models.ForeignKey(
        Loan,
        verbose_name='Préstamo',
        on_delete=models.CASCADE,
        related_name='related_payments'
    )
    value = models.FloatField(
        'Valor del pago'
    )
    date = models.DateField(
        'Fecha del pago',

    )

    def __str__(self):
        return "Pago de {}".format(self.loan)

    class Meta:
        verbose_name = 'Pago del préstamo'
        verbose_name_plural = 'Pagos del préstamo'
