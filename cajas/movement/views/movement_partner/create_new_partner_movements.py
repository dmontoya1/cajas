
from datetime import datetime

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxPartner
from concepts.models.concepts import Concept
from cajas.users.models.partner import PartnerType

from ...models.movement_partner import MovementPartner
from ..movement_don_juan.movement_don_juan import MovementDonJuan
from .create_movement_service_simple import CreateMovementSimpleService


class CreateNewPartnerMovements(object):

    def __init__(self, data):
        self._partner = data['partner']
        self._value = data['value']
        self._responsible = data['responsible']
        self._ip = data['ip']

    def call(self):
        concept = Concept.objects.get(name='Aporte Socio', concept_type='SD')
        data1 = {
            'box': self._partner.box,
            'concept': concept,
            'movement_type': 'IN',
            'value': self._value,
            'detail': 'Aporte Inicial Socio',
            'date': datetime.now(),
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement1 = CreateMovementSimpleService(data1).call()
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            data2 = {
                'box': box_don_juan,
                'concept': concept,
                'movement_type': 'OUT',
                'value': int(self._value)*2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(self._partner),
                'date': datetime.now(),
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = MovementDonJuan.create(data2)
        elif self._partner.partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=self._partner.direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': concept,
                'movement_type': 'OUT',
                'value': int(self._value)*2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(self._partner),
                'date': datetime.now(),
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = CreateMovementSimpleService(data2).call()
        data3 = {
            'box': self._partner.box,
            'concept': concept,
            'movement_type': 'IN',
            'value': int(self._value)*2,
            'detail': 'Aporte Inicial Socio directo',
            'date': datetime.now(),
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement3 = CreateMovementSimpleService(data3).call()

        return movement1
