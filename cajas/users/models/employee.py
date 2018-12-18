
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

def user_passport_path(instance, filename, name):
    return 'archivos/{0}/passport/{1}'.format(instance.user.document_id, filename)

def user_cv_path(instance, filename, name):
    return 'archivos/{0}/cv/{1}'.format(instance.user.document_id, filename)


class Employee(models.Model):

    PRESIDENTE = 'PRESI'
    SUBGERENTE = 'SUBGER'
    ASISTENTE_ADMIN = 'ASADMI'
    ADMIN_SENIOR = 'ASENI'
    ADMIN_JUNIOR = 'AJUNI'
    SECRETARIA = 'SECRE'
    SUPERVISOR = 'SUPERV'
    COBRADOR = 'COBRA'
    TARJETERO = 'TARJET'

    EMPLOYEE_TYPES = (
        (PRESIDENTE, 'Presidente'),
        (SUBGERENTE, 'Subgerente'),
        (ASISTENTE_ADMIN, 'Asistente Administrativa'),
        (ADMIN_SENIOR, 'Administrador Senior'),
        (ADMIN_JUNIOR, 'Administrador Junior'),
        (SECRETARIA, 'Secretaria'),
        (SUPERVISOR, 'Supervisor'),
        (COBRADOR, 'Cobrador'),
        (TARJETERO, 'Tarjetero')
    )

    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )
    passport = models.FileField(
        'Pasaporte',
        upload_to=user_passport_path
    )
    cv = models.FileField(
        'Hoja de vida',
        upload_to=user_cv_path
    )
    employee_type = models.CharField(
        'Tipo de empleado',
        max_length=10,
        choices=EMPLOYEE_TYPES
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'


    def __str__(self):
        return 'Empleado {} con cargo {}'.format(self.user.get_full_name(), self.get_employee_type_display())



    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'