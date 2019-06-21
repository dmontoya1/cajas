
from django.contrib.auth import get_user_model
from django.db import models

from cajas.general_config.models.country import Country
from cajas.concepts.models.concepts import Concept
from cajas.users.models.charges import Charge

User = get_user_model()


class Stop(models.Model):
    """Clase para guardar los topes de los conceptos por pais, ciudad y usuario
    """

    value = models.IntegerField(
        'Valor del tope',
    )
    concept = models.ForeignKey(
        Concept,
        verbose_name='Concepto',
        on_delete=models.CASCADE,
    )
    country = models.ForeignKey(
        Country,
        verbose_name='Pais',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Socio, empleado',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    charge = models.ForeignKey(
        Charge,
        verbose_name='Cargo',
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    is_informative = models.BooleanField(
        "Tope informativo?",
        default=False
    )
    report_by_charge = models.ForeignKey(
        Charge,
        verbose_name='Informar por cargo',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="related_charge_report"
    )
    report_users = models.ManyToManyField(
        User,
        verbose_name='Informar usuarios',
        related_name="related_users_report",
    )

    def __str__(self):
        if self.user:
            return 'Tope de %s para %s' % (self.concept.name, self.user.get_full_name())
        return 'Tope de %s para %s' % (self.concept.name, self.charge.name)

    class Meta:
        verbose_name = 'Tope'
