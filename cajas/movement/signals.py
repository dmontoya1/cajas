# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from cajas.boxes.models.box_partner import BoxStatus

from .models.movement_box_colombia import MovementBoxColombia
from .models.movement_daily_square import MovementDailySquare
from .models.movement_don_juan import MovementDonJuan
from .models.movement_don_juan_usd import MovementDonJuanUsd
from .models.movement_office import MovementOffice
from .models.movement_partner import MovementPartner
from .models.movement_provisioning import MovementProvisioning


@receiver(post_save, sender=MovementBoxColombia)
def save_balance_box_colombia(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_office.balance:
            l_balance = instance.box_office.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementBoxColombia.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_office.balance = instance.balance
        instance.box_office.last_movement_id = instance.pk
        instance.box_office.save()
        instance.save()


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


@receiver(post_save, sender=MovementPartner)
def save_balance_partner(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_partner.balance:
            l_balance = instance.box_partner.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementPartner.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_partner.balance = instance.balance
        instance.box_partner.last_movement_id = instance.pk
        instance.box_partner.save()
        instance.save()


@receiver(post_save, sender=MovementOffice)
def save_balance_office(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_office.balance:
            l_balance = instance.box_office.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementOffice.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_office.balance = instance.balance
        instance.box_office.last_movement_id = instance.pk
        instance.box_office.save()
        instance.save()


@receiver(post_save, sender=MovementDonJuan)
def save_balance_donjuan(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_don_juan.balance:
            l_balance = instance.box_don_juan.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementDonJuan.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_don_juan.balance = instance.balance
        instance.box_don_juan.last_movement_id = instance.pk
        instance.box_don_juan.save()
        instance.save()


@receiver(post_save, sender=MovementDonJuanUsd)
def save_balance_donjuan_usd(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_don_juan.balance:
            l_balance = instance.box_don_juan.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementDonJuan.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_don_juan.balance = instance.balance
        instance.box_don_juan.last_movement_id = instance.pk
        instance.box_don_juan.save()
        instance.save()


@receiver(post_save, sender=MovementProvisioning)
def save_balance_provisioning(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        if instance.box_provisioning.balance:
            l_balance = instance.box_provisioning.balance
        else:
            l_balance = 0

        if instance.movement_type == MovementDonJuan.IN:
            instance.balance = int(l_balance) + int(instance.value)
        else:
            instance.balance = int(l_balance) - int(instance.value)
        instance.box_provisioning.balance = instance.balance
        instance.box_provisioning.last_movement_id = instance.pk
        instance.box_provisioning.save()
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


@receiver(pre_delete, sender=MovementDonJuanUsd)
def delete_movement_usd_don_juan(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_don_juan
    if instance.movement_type == MovementDonJuanUsd.IN:
        box.balance -= instance.value
    else:
        box.balance += instance.value
    box.save()


@receiver(pre_delete, sender=MovementBoxColombia)
def delete_movement_box_colombia(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_office
    if instance.movement_type == MovementBoxColombia.IN:
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


@receiver(post_save, sender=MovementPartner)
def inactive_partner_box(sender, **kwargs):
    instance = kwargs.get('instance')
    box = instance.box_partner
    if box.box_status == BoxStatus.EN_LIQUIDACION and box.balance == instance.value:
        box.box_status = BoxStatus.LIQUIDADA
        box.save()
