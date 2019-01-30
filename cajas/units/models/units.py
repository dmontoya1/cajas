
from django.contrib.auth import get_user_model
from django.db import models

from cajas.users.models.partner import Partner
User = get_user_model()


class Unit(models.Model):
    """
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name='Socio',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_units'
    )
    collector = models.ForeignKey(
        User,
        verbose_name='Cobrador',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_collector_units'
    )
    supervisor = models.ForeignKey(
        User,
        verbose_name='Supervisor',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='related_supervisor_units'
    )
    is_active = models.BooleanField(
        'Unidad Activa',
        default=True
    )


    def __str__(self):
        return 'Unidad %s de %s' % (self.name, self.partner.get_full_name())


    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
