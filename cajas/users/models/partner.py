
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


class Partner(models.Model):

    DIRECTO = 'DIR'
    INDIRECTO = 'INDIR'

    PARTNER_TYPE = (
        (DIRECTO, 'Directo'),
        (INDIRECTO, 'Indirecto')
        
    )

    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )
    code = models.CharField(
        'Código',
        max_length=255,
    )
    partner_type = models.CharField(
        'Tipo de empleado',
        max_length=10,
        choices=PARTNER_TYPE,
    )
    direct_partner = models.ForeignKey(
        'self',
        verbose_name='Socio Directo',
        on_delete=models.CASCADE,
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'


    def __str__(self):
        return 'Socio {}'.format(self.get_full_name())


    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
