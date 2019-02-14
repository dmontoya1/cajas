
from django.db import models
from django.utils.text import slugify

from general_config.models.country import Country
from cajas.users.models.employee import Employee


class Office(models.Model):
    """Guarda los paises en donde el negocio tiene funcionamiento
    """

    country = models.ForeignKey(
        Country,
        verbose_name='Pais',
        on_delete=models.CASCADE
    )
    number = models.IntegerField(
        'Número de la oficina',
        default=1
    )
    admin_senior = models.OneToOneField(
        Employee,
        verbose_name='Adminsitrador Senior',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_senior_office'
    )
    admin_junior = models.OneToOneField(
        Employee,
        verbose_name='Adminsitrador Junior',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_junior_office'
    )
    secretary = models.OneToOneField(
        Employee,
        verbose_name='Secretaria',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_secretary_office'
    )
    phone_number = models.CharField(
        'Telefono',
        max_length=255,
        blank=True, null=True
    )
    address = models.CharField(
        'Direccion',
        max_length=255,
        blank=True, null=True
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        null=True,
        blank=True,
    )
    consecutive = models.IntegerField(
        'Consecutivo Socios',
        default=1
    )

    def __str__(self):
        if self.country:
            return '{}{} - {}'.format(self.country.abbr, self.number, self.country.name)
        return "Oficina"

    def save(self, *args, **kwargs):
        text = '{}{}'.format(self.country.abbr, self.number)
        self.slug = slugify(text)
        super(Office, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'
