# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from boxes.models.box_office import BoxOffice

from office.models.office import Office

@receiver(post_save, sender=Office)
def create_office_box(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        try:
            box1 = BoxOffice(
                office=instance,
            )
            box1.save()
        except Exception as e:
            print (e)
