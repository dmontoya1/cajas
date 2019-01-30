from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from cajas.users.models.user import User


class AuthLogs(models.Model):
    """Guarda los logs de cada inicio y cierre de sesión de la plataforma
    """

    LOGIN = 'LI'
    LOGOUT = 'LO'

    ACTION = (
        (LOGIN, 'Inicio de sesión'),
        (LOGOUT, 'Cierre de sesión')
    )

    date = models.DateTimeField(
        "Fecha",
        auto_now=True
    )
    ip = models.GenericIPAddressField(
        "Dirección IP", 
        protocol='both'
    )
    action = models.CharField(
        'Acción',
        max_length=5,
        choices=ACTION
    )
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        related_name="related_logs",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "Log de {}".format(self.user)

    class Meta:
        verbose_name = "Log de autenticación"
        verbose_name_plural = "Logs de autenticación"
