# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from tenant_schemas.signals import post_schema_sync
from tenant_schemas.utils import tenant_context


from cajas.boxes.models.box_office import BoxOffice
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.boxes.models.box_provisioning import BoxProvisioning
from cajas.tenant.models import Platform
from cajas.users.models.partner import Partner
from cajas.webclient.views.utils import get_president_user

from .models.officeCountry import OfficeCountry

president = get_president_user()


def create_office_country_box(sender, tenant, **kwargs):
    tenant1 = Platform(schema_name=tenant.schema_name)
    with tenant_context(tenant1):
        if kwargs.get('created'):
            instance = kwargs.get('instance')
            BoxOffice.objects.create(
                office=instance,
            )
            schema_name = connection.schema_name
            print(schema_name)
            print(president)
            donjuan = Partner.objects.get(user=president)
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


post_schema_sync.connect(create_office_country_box, sender=OfficeCountry)
