from django.db import models

from cajas.users.models.partner import Partner


class BoxPartner(models.Model):
    """Modelo para la caja de un socio
    """

    partner = models.OneToOneField(
        Partner,
        verbose_name='Socio',
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
        if self.partner is not None:
            return "Caja de {}".format(self.partner.user.get_full_name())
        return "Caja de usuario eliminado"

    class Meta:
        verbose_name = 'Caja de socio'
        verbose_name_plural = 'Cajas de socios'
