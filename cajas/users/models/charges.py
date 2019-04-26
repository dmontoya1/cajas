from django.db import models


class Charge(models.Model):
    """Guarda los cargos disponibles en la empresa
    """

    name = models.CharField(
        'Nombre',
        max_length=255,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cargo'
