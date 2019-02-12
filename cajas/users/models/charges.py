from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Charge(models.Model):
    """Guarda los cargos disponibles en la empresa
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cargo'
