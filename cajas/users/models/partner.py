
from django.contrib.auth import get_user_model
from django.db import models

from enumfields import EnumField
from enumfields import Enum

from office.models.office import Office

User = get_user_model()


def user_passport_path(instance, filename, name):
    return 'archivos/{0}/passport/{1}'.format(instance.user.document_id, filename)


def user_cv_path(instance, filename, name):
    return 'archivos/{0}/cv/{1}'.format(instance.user.document_id, filename)


class PartnerType(Enum):
    DIRECTO = 'DIR'
    INDIRECTO = 'INDIR'
    DONJUAN = 'DJ'

    class Labels:
        DIRECTO = 'Directo'
        INDIRECTO = 'Indirecto'
        DONJUAN = 'Don Juan'


class Partner(models.Model):

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
    partner_type = EnumField(
        PartnerType,
        verbose_name='Tipo de socio',
        max_length=5,
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
    consecutive = models.IntegerField(
        'Consecutivo Mini-Socios',
        default=1
    )

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

    def __str__(self):
        return 'Socio {} ({})'.format(self.get_full_name(), self.code)

    def save(self, *args, **kwargs):
        "Funcion para generar el código del socio"
        if not self.code:
            if self.partner_type != PartnerType.DONJUAN':
                self.code = '{}{}-{}'.format(self.office.country.abbr, self.office.number, self.office.consecutive)
            else:
                self.code = 'DONJUAN'
            self.office.consecutive += 1
            self.office.save()
        super(Partner, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        unique_together = ("office", "user")
