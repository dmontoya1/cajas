
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

from cajas.users.models.charges import Charge
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry

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

    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE,
        related_name='related_employee'
    )
    charge = models.ForeignKey(
        Charge,
        verbose_name='Cargo de empleado',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    office = models.ManyToManyField(
        Office,
        verbose_name='Oficina',
        related_name='related_employees',
        blank=True
    )
    office_country = models.ManyToManyField(
        OfficeCountry,
        verbose_name='Oficina por País',
        related_name='related_employees',
        blank=True
    )
    salary_type = models.CharField(
        'Tipo de salario',
        max_length=2,
        choices=SALARY_TYPE,
        default=FIXED
    )
    salary = models.FloatField(
        'Salario Empleado',
        default=0
    )
    passport = models.FileField(
        'Pasaporte',
        upload_to=user_passport_path,
        blank=True,
        null=True
    )
    cv = models.FileField(
        'Hoja de vida',
        upload_to=user_cv_path,
        blank=True,
        null=True
    )
    observations = models.TextField(
        'Motivo de despido',
        help_text='Motivo para deshabilitar el empleado',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return '{}'.format(self.user.get_full_name())

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

    def is_admin_charge(self):
        charge_secretary = Charge.objects.get(name='Secretaria')
        charge_admin_senior = Charge.objects.get(name='Administrador Senior')
        if self.charge == charge_secretary or self.charge == charge_admin_senior:
            return True
        return False
