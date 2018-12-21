from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


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
        unique=True
    )
    is_abstract = models.BooleanField(
        "Tiene acceso a la plataforma?",
        default=True
    )

    def __str__(self):
        # if self.partner:
        #     return "{} ({})".format(self.get_full_name(), self.partnet.code)
        return "{} ({})".format(self.get_full_name(), self.document_id)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
