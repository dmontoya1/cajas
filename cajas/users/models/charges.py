from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

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
