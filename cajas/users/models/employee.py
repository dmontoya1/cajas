
from django.contrib.auth import get_user_model
from django.db import models

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
    salary_type = models.CharField(
        'Tipo de salario',
        max_length=2,
        choices=SALARY_TYPE,
        default=FIXED
    )
    salary = models.IntegerField(
        'Salario Empleado',
        default=0
    )
    passport = models.FileField(
        'Pasaporte',
        upload_to=user_passport_path
    )
    cv = models.FileField(
        'Hoja de vida',
        upload_to=user_cv_path
    )
    is_daily_square = models.BooleanField(
        'Es cuadre diario?',
        default=False
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

    def __str__(self):
        return '{}'.format(self.user.get_full_name())

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
