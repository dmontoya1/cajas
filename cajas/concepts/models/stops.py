
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db import models

from general_config.models.country import Country
from concepts.models.concepts import Concept
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


    def __str__(self):
        if self.user:
            return 'Tope de %s para %s' % (self.concept.name, self.user.get_full_name())
        return 'Tope de %s para %s' % (self.concept.name, self.charge.name)


    class Meta:
        verbose_name = 'Tope'
