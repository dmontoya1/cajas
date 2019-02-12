# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from cajas.users.models.partner import Partner
from boxes.models.box_office import BoxOffice
from boxes.models.box_don_juan import BoxDonJuan
from office.models.office import Office


@receiver(post_save, sender=Office)
def create_office_box(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        box1 = BoxOffice(
            office=instance,
        )
        box1.save()
        donjuan = Partner.objects.get(code='DONJUAN')
        box_don_juan = BoxDonJuan(
            partner=donjuan,
            office=instance
        )
        box_don_juan.save()
