from django.db import models

from cajas.users.models.user import User


class BoxDailySquare(models.Model):
    """Modelo para la caja de un cuadre diario
    """

    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    balance = models.IntegerField(
        "Saldo de la caja",
        default=0
    )
    is_active = models.BooleanField(
        "Caja Activa?",
        default=True
    )
    last_movement_id = models.IntegerField(
        'id último movimiento',
        default=0
    )

    def __str__(self):
        if self.user:
            return "Caja de {}".format(self.user.get_full_name())
        return "Caja de cuadre diario"

    class Meta:
        verbose_name = 'Caja de Cuadre Diario'
        verbose_name_plural = 'Cajas de Cuadre Diario'
