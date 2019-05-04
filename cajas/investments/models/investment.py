
from django.db import models

from cajas.users.models.partner import Partner


class Investment(models.Model):

    PERSONAL = 'PE'
    BUSINESS = 'BS'

    INVESTMENT_TYPE = (
        (PERSONAL, 'Personal'),
        (BUSINESS, 'Negocio')
    )

    partner = models.ForeignKey(
        Partner,
        verbose_name='Socio',
        related_name='related_investments',
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        'Fecha',
        auto_now=False
    )
    element = models.TextField(
        'Elemento que se negocia'
    )
    total_value = models.IntegerField(
        'Valor Total'
    )
    balance = models.IntegerField(
        'Saldo a la fecha',
        default=0
    )
    conditions = models.TextField(
        'Condiciones de la negociación'
    )
    initial_value = models.IntegerField(
        'Cuota inicial',
    )
    monthly_pay = models.IntegerField(
        'Valor pago mensual',
        default=0
    )
    time = models.IntegerField(
        'Plazo (en meses)',
        blank=True,
        null=True
    )
    investment_type = models.CharField(
        'Tipo de inversión',
        max_length=2,
        choices=INVESTMENT_TYPE,
    )

    def __str__(self):
        return "Inversión {}".format(self.partner)

    def get_investment_pay(self):
        if self.monthly_pay > 0:
            return self.monthly_pay

    class Meta:
        verbose_name = 'Inversión Negocios'
        verbose_name_plural = 'Inversiones Negocios'
