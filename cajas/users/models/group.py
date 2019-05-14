from django.db import models
from .employee import Employee


class Group(models.Model):
    """Guarda la relacion del Administrador de Grupo con sus supervisores
    """

    admin = models.OneToOneField(
        Employee,
        verbose_name='Administrador de Grupo',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Administrador {}".format(self.admin.user)

    class Meta:
        verbose_name = 'Administrador de grupo'
