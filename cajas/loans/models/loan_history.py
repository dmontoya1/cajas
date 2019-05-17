from django.db import models

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
        (LOAN, 'Prestamo'),
        (INTEREST, 'Interes'),
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
    date = models.DateField(
        'Fecha del pago',

    )

    def __str__(self):
        if self.history_type:
            return "{} de {}".format(self.get_history_type_display(), self.loan)
        return "Pago de {}".format(self.loan)

    def save(self, *args, **kwargs):
        loan = self.loan
        if self.history_type == self.ABONO:
            loan.balance -= float(self.value)
        elif self.history_type == self.LOAN:
            loan.balance += float(self.value)
        loan.save()
        super(LoanHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Historial de préstamo'
        verbose_name_plural = 'Historial de préstamos'
