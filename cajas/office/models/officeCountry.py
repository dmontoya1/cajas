
from django.db import models
from django.utils.text import slugify

from general_config.models.country import Country

from .office import Office


class OfficeCountry(models.Model):

    office = models.ForeignKey(
        Office,
        verbose_name='Oficina',
        on_delete=models.CASCADE,
        related_name='related_office_country'
    )
    country = models.ForeignKey(
        Country,
        verbose_name='País',
        on_delete=models.SET_NULL,
        null=True,
        related_name='related_office_country'
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Oficina por país'
        verbose_name_plural = 'Oficinas por país'

    def __str__(self):
        return "Oficina {} - {}".format(self.office.number, self.country)

    def save(self, *args, **kwargs):
        text = '{}{}'.format(self.country.abbr, self.office.number)
        self.slug = slugify(text)
        super(OfficeCountry, self).save(*args, **kwargs)
