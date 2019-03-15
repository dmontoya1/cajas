
from django.contrib.auth import get_user_model
from django.db import models

from .chain_place import ChainPlace

User = get_user_model()


class UserPlace(models.Model):
    """
    """

    chain_place = models.ForeignKey(
        ChainPlace,
        verbose_name='Puesto de la cadena',
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.SET_NULL,
        related_name='related_chains',
        null=True, blank=True
    )
    place_porcentaje = models.FloatField(
        'Porcentaje del usuario',

    )

    def __str__(self):
        return "Puesto de {} de la cadena {}".format(self.user, self.chain_place.chain)

    def get_user_value(self):
        return (self.place_porcentaje * self.chain_place.chain.place_value) / 100

    class Meta:
        verbose_name = "Usuario por puesto"
        verbose_name_plural = "Usuarios por puesto"
        ordering = ['id']
