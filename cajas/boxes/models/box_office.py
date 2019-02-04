from django.contrib.auth import get_user_model
from django.db import models

from office.models.office import Office


class BoxOffice(models.Model):
    """Modelo para la caja de la oficina de un país
    """

    office = models.OneToOneField(
        Office,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='box'
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
        try:
            return "Caja de {}".format(self.office.name)
        except:
            return "Caja de oficina"


    class Meta:
        verbose_name = 'Caja de oficinas'
        verbose_name_plural = 'Cajas de Oficina'
