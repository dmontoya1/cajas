# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.country import Country
from .models.currency import Currency


# @receiver(post_save, sender=Country)
# def create_country_boxes(sender, **kwargs):
#     if kwargs.get('created'):
#         instance = kwargs.get('instance')
#         box1 = BoxCountry(
#             country=instance,
#             currency=instance.currency
#         )
#         box1.save()
#         usd_dolar, created = Currency.objects.get_or_create(
#             name='Dólar Americano',
#             abbr='USD',
#         )
#         box2 = BoxCountry(
#             country=instance,
#             currency=usd_dolar
#         )
#         box2.save()
