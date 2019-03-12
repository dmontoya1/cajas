
from django.db import models

from .chain_place import ChainPlace


class UserPlace(models.Model):
    """

    """

    chain_place = models.ForeignKey(
        ChainPlace,
        verbose_name='Puesto de la cadena',
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    


