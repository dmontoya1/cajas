# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from cajas.users.models.partner import Partner
from cajas.boxes.models.box_office import BoxOffice
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.boxes.models.box_provisioning import BoxProvisioning

from .models.officeCountry import OfficeCountry


@receiver(post_save, sender=OfficeCountry)
def create_office_country_box(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        BoxOffice.objects.create(
            office=instance,
        )
        donjuan = Partner.objects.get(code='DONJUAN')
        BoxDonJuan.objects.create(
            partner=donjuan,
            office=instance
        )
        BoxDonJuanUSD.objects.create(
            partner=donjuan,
            office=instance
        )
        BoxProvisioning.objects.create(
            office=instance,
        )
