
from datetime import datetime

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxPartner
from concepts.models.concepts import Concept
from cajas.users.models.partner import PartnerType

from ...models.movement_partner import MovementPartner
from ..movement_don_juan.movement_don_juan import MovementDonJuan
from .create_movement_service_simple import CreateMovementSimpleService


class CreateMovementSimpleDoubleService(object):

    def __init__(self, partner, concept, movement_type, value, detail, date, responsible, ip):
        self._partner = partner
        self._concept = concept
        self._movement_type = movement_type
        self._value = value
        self._detail = detail
        self._date = date
        self._responsible = responsible
        self._ip = ip

    def call(self):
        movement1 = CreateMovementSimpleService(
            self._partner.box,
            self._concept,
            self._movement_type,
            self._value,
            self._detail,
            self._date,
            self._responsible,
            self._ip
        ).call()
        if self._movement_type == 'IN':
            contrapart = 'OUT'
        else:
            contrapart = 'IN'
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            movement2 = MovementDonJuan.create(
                box_don_juan,
                self._concept,
                contrapart,
                self._value,
                self._detail,
                self._date,
                self._responsible,
                self._ip
            )
        elif self._partner.partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=self._partner.direct_partner)
            movement2 = CreateMovementSimpleService(
                box_direct_partner,
                self._concept,
                contrapart,
                self._value,
                self._detail,
                self._date,
                self._responsible,
                self._ip
            ).call()
        movement3 = CreateMovementSimpleService(
            self._partner.box,
            self._concept,
            self._movement_type,
            self._value,
            self._detail,
            self._date,
            self._responsible,
            self._ip
        ).call()

        return movement1
