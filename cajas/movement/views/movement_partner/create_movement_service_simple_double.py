
from datetime import datetime

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_partner import BoxPartner
from cajas.concepts.models.concepts import Concept
from cajas.users.models.partner import PartnerType

from ...services.don_juan_service import DonJuanManager
from .create_movement_service_simple import CreateMovementSimpleService

donjuan_manager = DonJuanManager()


class CreateMovementSimpleDoubleService(object):

    def __init__(self, data):
        self._partner = data['partner']
        self._concept = data['concept']
        self._movement_type = data['movement_type']
        self._value = data['value']
        self._detail = data['detail']
        self._date = data['date']
        self._responsible = data['responsible']
        self._ip = data['ip']

    def call(self):
        data1 = {
            'box': self._partner.box,
            'concept': self._concept,
            'movement-type': self._movement_type,
            'value': self._value,
            'detail': self._detail,
            'date': self._date,
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement1 = CreateMovementSimpleService(data1).call()
        if self._movement_type == 'IN':
            contrapart = 'OUT'
        else:
            contrapart = 'IN'
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            data2 = {
                'box': box_don_juan,
                'concept': self._concept,
                'movement_type': contrapart,
                'value': self._value,
                'detail': self._detail,
                'date': self._date,
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = donjuan_manager.create_movement(data2)
        elif self._partner.partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=self._partner.direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': self._concept,
                'movement-type': contrapart,
                'value': self._value,
                'detail': self._detail,
                'date': self._date,
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = CreateMovementSimpleService(data2).call()
        data3 = {
            'box': self._partner.box,
            'concept': self._concept,
            'movement-type': contrapart,
            'value': self._value,
            'detail': self._detail,
            'date': self._date,
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement3 = CreateMovementSimpleService(data3).call()

        return movement1
