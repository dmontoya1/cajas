
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from general_config.models.country import Country

User = get_user_model()


class Office(models.Model):
    """Guarda los paises en donde el negocio tiene funcionamiento
    """


    name = models.CharField(
        'Nombre',
        max_length=255,
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
    country = models.ForeignKey(
        Country,
        verbose_name='Pais',
        on_delete=models.CASCADE
    )
    admin_senior = models.OneToOneField(
        User,
        verbose_name='Adminsitrador Senior',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_senior_office'
    )
    admin_junior = models.OneToOneField(
        User,
        verbose_name='Adminsitrador Junior',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_junior_office'
    )
    secretary = models.OneToOneField(
        User,
        verbose_name='Secretaria',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_secretary_office'
    )

    def __str__(self):
        return '{} - {}'.format(self.name, self.country.name)


    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'
