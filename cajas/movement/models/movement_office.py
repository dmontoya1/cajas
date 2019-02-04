from django.db import models

from boxes.models.box_office import BoxOffice
from .movement_mixin import MovementMixin


class MovementOffice(MovementMixin):
    """Modelo para guardar los movimientos de las cajas de la oficina
    """

    box_office = models.ForeignKey(
        BoxOffice,
        verbose_name='Caja oficina',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='movements'
    )

    def __str__(self):
        return "Movimiento de {}".format(self.box_office.office)

    
    def save(self, *args, **kwargs):
        try:
            l_balance = self.box_office.balance
        except Exception as e:
            print (e)
            l_balance = 0
        
        if self.movement_type == MovementOffice.IN:
            self.balance = int(l_balance) + int(self.value)
        else:
            self.balance = int(l_balance) - int(self.value)

        super(MovementOffice, self).save(*args, **kwargs)
        self.box_office.balance = self.balance
        self.box_office.last_movement_id = self.pk
        self.box_office.save()


    class Meta:
        verbose_name = 'Movimiento de la oficina'
        verbose_name_plural = 'Movimientos de la oficina'
