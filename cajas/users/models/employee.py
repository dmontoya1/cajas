
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from cajas.users.models.charges import Charge
from office.models.office import Office
from webclient.views.utils import get_object_or_none

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
    is_daily_square = models.BooleanField(
        'Es cuadre diario?',
        default=False
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

    def __str__(self):
        return '{}'.format(self.user.get_full_name())

    # def save(self, *args, **kwargs):
    #     charge_secretary = Charge.objects.get(name='Secretaria')
    #     charge_admin_senior = Charge.objects.get(name='Administrador Senior')
    #     secretary = get_object_or_none(Employee, charge=charge_secretary, office=self.office)
    #     admin_senior = get_object_or_none(Employee, charge=charge_admin_senior, office=self.office)
    #     if self.charge == charge_secretary and not secretary:
    #         super(Employee, self).save(*args, **kwargs)
    #     else:
    #         raise ValidationError('Ya existe una secretaria para esta oficina')

    #     if self.charge == charge_admin_senior and not admin_senior:
    #         super(Employee, self).save(*args, **kwargs)
    #     else:
    #         raise ValidationError('Ya existe un administrador senior para esta oficina')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
