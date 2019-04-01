
from django.db import models

from ..models.user_place import UserPlace


class UserPlacePay(models.Model):
    """
    """

    user_place = models.ForeignKey(
        UserPlace,
        verbose_name='Puesto del usuario',
        related_name='related_payments',
        on_delete=models.CASCADE,
    )
    pay_value = models.FloatField(
        'Valor del pago',
    )
    date = models.DateField(
        'Fecha del pago'
    )

    def __str__(self):
        return "Pago del {}".format(self.user_place)

    class Meta:
        verbose_name = "Pago del puesto"
        verbose_name_plural = "Pagos del puesto"
