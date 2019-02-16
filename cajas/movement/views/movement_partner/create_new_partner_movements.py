
from datetime import datetime

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxPartner
from concepts.models.concepts import Concept
from cajas.users.models.partner import PartnerType

from ...models.movement_partner import MovementPartner
from ..movement_don_juan.movement_don_juan import MovementDonJuan
from .create_movement_service_simple import CreateMovementSimpleService


class CreateNewPartnerMovements(object):

    def __init__(self, partner, value, responsible, ip):
        self._partner = partner
        self._value = value
        self._responsible = responsible
        self._ip = ip

    def call(self):
        concept = Concept.objects.get(name='Aporte Socio', concept_type='SD')
        movement1 = CreateMovementSimpleService(
            self._partner.box,
            concept,
            'IN',
            self._value,
            'Aporte Inicial Socio',
            datetime.now(),
            self._responsible,
            self._ip
        ).call()
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            movement2 = MovementDonJuan.create(
                box_don_juan,
                concept,
                'OUT',
                int(self._value)*2,
                'Salida Aporte Nuevo socio',
                datetime.now(),
                self._responsible,
                self._ip
            )
        elif self._partner.partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=self._partner.direct_partner)
            movement2 = CreateMovementSimpleService(
                box_direct_partner,
                concept,
                'OUT',
                int(self._value)*2,
                'Salida Aporte Nuevo socio',
                datetime.now(),
                self._responsible,
                self._ip
            ).call()
        movement3 = CreateMovementSimpleService(
            self._partner.box,
            concept,
            'IN',
            int(self._value)*2,
            'Aporte Inicial Socio directo',
            datetime.now(),
            self._responsible,
            self._ip
        ).call()

        return movement1
