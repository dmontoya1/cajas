from django.contrib.auth.models import AbstractUser
from django.db import models

from .charges import Charge


class User(AbstractUser):

    CEDULA_CIUDADANIA = 'CC'
    CEDULA_EXTRANJERA = 'CE'
    PASAPORTE = 'PA'

    DOCUMENT_TYPE = (
        (CEDULA_CIUDADANIA, 'Cédula de ciudadania'),
        (CEDULA_EXTRANJERA, 'Cédula de extranjería'),
        (PASAPORTE, 'Pasaporte'),
    )

    document_type = models.CharField(
        "Tipo Documento",
        max_length=3,
        choices=DOCUMENT_TYPE
    )
    document_id = models.CharField(
        "Número Documento",
        max_length=15,
        unique=False,
        default='',
    )
    is_daily_square = models.BooleanField(
        'Es cuadre diario?',
        default=False
    )
    is_abstract = models.BooleanField(
        "Tiene acceso a la plataforma?",
        default=True
    )

    def __str__(self):
        return "{} ({})".format(self.get_full_name(), self.document_id)

    def is_employee(self):
        try:
            if self.related_employee.get():
                return True
            return False
        except:
            return False

    def is_secretary(self):
        secretary = Charge.objects.get(name="Secretaria")
        if self.related_employee.get().charge == secretary:
            return True
        return False
