
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from office.models.office import Office

User = get_user_model()

def user_passport_path(instance, filename, name):
    return 'archivos/{0}/passport/{1}'.format(instance.user.document_id, filename)

def user_cv_path(instance, filename, name):
    return 'archivos/{0}/cv/{1}'.format(instance.user.document_id, filename)


class Partner(models.Model):

    DIRECTO = 'DIR'
    INDIRECTO = 'INDIR'
    DONJUAN = 'DJ'

    PARTNER_TYPE = (
        (DIRECTO, 'Directo'),
        (INDIRECTO, 'Indirecto'),
        (DONJUAN, 'Don Juan')
    )

    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE,
        related_name='partner'
    )
    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.SET_NULL,
        blank=True, 
        null=True
    )
    code = models.CharField(
        'Código',
        max_length=255,
        blank=True,
        null=True
    )
    partner_type = models.CharField(
        'Tipo de socio',
        max_length=10,
        choices=PARTNER_TYPE,
    )
    direct_partner = models.ForeignKey(
        'self',
        verbose_name='Socio Directo',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    is_daily_square = models.BooleanField(
        'Es cuadre diario?',
        default=False
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'


    def __str__(self):
        return 'Socio {} ({})'.format(self.get_full_name(), self.code)
    
    def save(self, *args, **kwargs):
        "Funcion para generar el código del socio, y para validar que solo este en una oficina por país"
        try:
            if not self.code:
                if self.partner_type != self.DONJUAN:
                    self.code = '{}{}-{}'.format(self.office.country.abbr, self.office.number, self.office.consecutive)
                else:
                    self.code = '{}{}-{}'.format(self.office.country.abbr, self.office.number, 'DJ')
                self.office.consecutive += 1
                self.office.save()
            print (self.code)
        except:
            pass
        super(Partner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        unique_together = ("office", "user")
