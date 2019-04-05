
from django.db import models

from .investment import Investment


class InvestmentPay(models.Model):

    investment = models.ForeignKey(
        Investment,
        verbose_name='Inversión',
        related_name='related_pays',
        on_delete=models.CASCADE
    )
    value = models.IntegerField(
        'Valor del pago'
    )
    detail = models.TextField(
        'Detalle del pago',
        default=''
    )
    date = models.DateField(
        'Fecha del pago',
        auto_now_add=False
    )

    def __str__(self):
        return "Pago de {}".format(self.investment)

    class Meta:
        verbose_name = 'Pago de Inversión'
        verbose_name_plural = 'Pagos de Inversión'
