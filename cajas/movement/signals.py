# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.movement_daily_square import MovementDailySquare

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
