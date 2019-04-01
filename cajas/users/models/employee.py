
from django.contrib.auth import get_user_model
from django.db import models

from cajas.users.models.charges import Charge
from office.models.office import Office

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
        on_delete=models.CASCADE,
        related_name='employee'
    )
    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.CASCADE,
        related_name='related_employees',
        null=True, blank=True
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
    observations = models.TextField(
        'Motivo de despido',
        help_text='Motivo para deshabilitar el empleado',
        blank=True, null=True
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

    def __str__(self):
        return '{}'.format(self.user.get_full_name())

    def is_admin_charge(self):
        charge_secretary = Charge.objects.get(name='Secretaria')
        charge_admin_junior = Charge.objects.get(name='Administrador Junior')
        charge_admin_senior = Charge.objects.get(name='Administrador Senior')
        if self.charge == charge_admin_junior or self.charge == charge_secretary or self.charge == charge_admin_senior:
            return True
        return False

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
