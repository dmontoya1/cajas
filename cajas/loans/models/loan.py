from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from enumfields import EnumField
from enumfields import Enum

from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models import Partner

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
        'Saldo a la fecha',
    )
    balance_cop = models.FloatField(
        'Saldo a la fecha (En COP)',
        default=0
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
            return "Préstamo de {} a {}".format(
                self.provider.get_full_name(),
                self.lender.get_full_name(),
            )
        return "Préstamo de la oficina a {}".format(
            self.lender.get_full_name(),
        )

    def get_interest_payment(self):
        """Obtiene el pago del interes mensual del prestamo
        """
        return int((self.balance * self.interest) / 100)

    def get_interest_actual_month_payment(self):
        month = datetime.now().month
        interest = self.related_payments.filter(date__month=month, history_type='IN')
        if interest.exists():
            return True
        return False

    def get_lender_box_balance_positive(self):
        partner = Partner.objects.filter(user=self.lender, office=self.office).first()
        if partner:
            if partner.box.balance > 0:
                return True
            else:
                return False
        else:
            return True

    class Meta:
        verbose_name = 'Préstamo'
