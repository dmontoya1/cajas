# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from boxes.models.box_country import BoxCountry

from .models.country import Country
from .models.currency import Currency


@receiver(post_save, sender=Country)
def create_country_boxes(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        try:
            box1 = BoxCountry(
                country=instance,
                currency=instance.currency
            )
            box1.save()
        except Exception as e:
            print (e)
        usd_dolar, created = Currency.objects.get_or_create(
            name='Dólar Americano',
            abbr='USD',
        )
        try:
            box2 = BoxCountry(
                country=instance,
                currency=usd_dolar
            )
            box2.save()
        except Exception as e:
            print (e)