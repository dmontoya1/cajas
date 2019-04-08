# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models.movement_daily_square import MovementDailySquare
from .models.movement_don_juan import MovementDonJuan
from .models.movement_office import MovementOffice
from .models.movement_partner import MovementPartner
from .models.movement_provisioning import MovementProvisioning


@receiver(post_save, sender=MovementDailySquare)
def save_balance_daily_square(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_daily_square.balance:
            l_balance = instance.box_daily_square.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementDailySquare.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_daily_square.balance = instance.balance
        instance.box_daily_square.last_movement_id = instance.pk
        instance.box_daily_square.save()
        instance.save()


@receiver(pre_delete, sender=MovementDailySquare)
def delete_movement_daily_square(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_daily_square
    if instance.movement_type == MovementDailySquare.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()


@receiver(pre_delete, sender=MovementDonJuan)
def delete_movement_don_juan(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_don_juan
    if instance.movement_type == MovementDonJuan.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()


@receiver(pre_delete, sender=MovementOffice)
def delete_movement_office(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_office
    if instance.movement_type == MovementOffice.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()


@receiver(pre_delete, sender=MovementPartner)
def delete_movement_partner(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_partner
    if instance.movement_type == MovementPartner.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()


@receiver(pre_delete, sender=MovementProvisioning)
def delete_movement_provisioning(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_provisioning
    if instance.movement_type == MovementProvisioning.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()
