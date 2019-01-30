
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from cajas.users.models.charges import Charge

User = get_user_model()

def user_passport_path(instance, filename):
    return 'archivos/{0}/passport/{1}'.format(instance.user.document_id, filename)

def user_cv_path(instance, filename):
    return 'archivos/{0}/cv/{1}'.format(instance.user.document_id, filename)


class Employee(models.Model):
    """
    """

    FIXED = 'FX'
    PERCENTAGE = 'PE'

    SALARY_TYPE = (
        (FIXED, 'Salario Fijo'),
        (PERCENTAGE, 'Porcentaje de comisión')
    )

    user = models.OneToOneField(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )
    charge = models.ForeignKey(
        Charge,
        verbose_name='Cargo de empleado',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    salary = models.IntegerField(
        'Salario Empleado',
        default=0
    )
    salary_type = models.CharField(
        'Tipo de salario',
        max_length=2,
        choices=SALARY_TYPE,
        default=FIXED
    )
    passport = models.FileField(
        'Pasaporte',
        upload_to=user_passport_path
    )
    cv = models.FileField(
        'Hoja de vida',
        upload_to=user_cv_path
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'


    def __str__(self):
        return 'Empleado {} con cargo {}'.format(self.user.get_full_name(), self.charge.name)


    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
