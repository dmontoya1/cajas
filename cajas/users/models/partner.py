
from django.contrib.auth import get_user_model
from django.db import models

from enumfields import EnumField
from enumfields import Enum

from office.models.officeCountry import OfficeCountry

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
        OfficeCountry,
        verbose_name='Oficina por País',
        related_name='partners',
        on_delete=models.SET_NULL,
        blank=True, null=True
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
    consecutive = models.IntegerField(
        'Consecutivo Mini-Socios',
        default=1
    )

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

    def __str__(self):
        return 'Socio {} ({})'.format(self.get_full_name(), self.code)

    def save(self, *args, **kwargs):
        "Funcion para generar el código del socio"
        if not self.code:
            if self.partner_type != PartnerType.DONJUAN:
                if self.partner_type == PartnerType.DIRECTO:
                    self.code = '{}{}-{}'.format(self.office.country.abbr, self.office.office.number, self.office.office.consecutive)
                    self.office.office.consecutive += 1
                    self.office.save()
                else:
                    self.code = '{}-{}'.format(self.direct_partner.code, self.direct_partner.consecutive)
                    self.direct_partner.consecutive += 1
                    self.direct_partner.save()
            else:
                self.code = 'DONJUAN'
        super(Partner, self).save(*args, **kwargs)

    def get_full_name(self):
        return '{}'.format(self.user.get_full_name())

    get_full_name.short_description = 'Nombres'

