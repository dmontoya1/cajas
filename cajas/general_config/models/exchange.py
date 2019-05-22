
from django.db import models

from .currency import Currency


class Exchange(models.Model):
    """ Modelo para guardar las tasas de cambio por cada divisa
    """

    currency = models.ForeignKey(
        Currency,
        verbose_name='Divisa',
        on_delete=models.CASCADE
    )

    month = models.DateField(
        'Mes',
        auto_now=False,
        auto_now_add=False,
        help_text='Ingresa el mes en el que tienen validez estas tasas de cambio'
    )
    exchange_dolar = models.FloatField(
        'Cambio divisa a Dolar (Prestamo)',
        help_text='Tasa de cambio para prestamos de la divisa a dolar'
    )
    exchange_cop = models.FloatField(
        'Factor divisa a Peso Colombiano (Prestamo)',
        help_text='Factor de cambio para prestamos de la divisa a peso colombiano'
    )
    exchange_dolar_abono = models.FloatField(
        'Cambio divisa a Dolar (Abonos)',
        help_text='Tasa de cambio para abonos e intereses de la divisa a dolar'
    )
    exchange_cop_abono = models.FloatField(
        'Factor divisa a Peso Colombiano (Abono)',
        help_text='Factor de cambio para abonos e intereses de la divisa a peso colombiano'
    )

    def __str__(self):
        return '%s (%s)' % (self.month, self.currency.name)

    class Meta:
        verbose_name = 'Tasa de cambio'
        verbose_name_plural = 'Tasas de cambio'
