
from datetime import datetime

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import PartnerType
from concepts.models.concepts import Concept, ConceptType

from ..models.movement_partner import MovementPartner
from ..services.don_juan_service import DonJuanManager

donjuan_manager = DonJuanManager()


class MovementPartnerManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def __init__(self, data):
        self._partner = data['partner']
        self._concept = data['concept']
        self._movement_type = data['movement_type']
        self._value = data['value']
        self._detail = data['detail']
        self._date = data['date']
        self._responsible = data['responsible']
        self._ip = data['ip']

    def create_simple(self, data):
        self.__validate_data(data)
        movement = MovementPartner.objects.create(
            box_partner=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip']
        )
        return movement

    def create_double(self, data):
        self.__validate_data(data)
        data1 = {
            'box': data['box'],
            'concept': data['concept'],
            'movement_type': data['movement_type'],
            'value': data['value'],
            'detail': data['detail'],
            'date': data['date'],
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement1 = self.create_simple(data1)
        if self._movement_type == 'IN':
            contrapart = 'OUT'
        else:
            contrapart = 'IN'
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            data2 = {
                'box': box_don_juan,
                'concept': self._concept.counterpart,
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
                'concept': self._concept.counterpart,
                'movement_type': contrapart,
                'value': self._value,
                'detail': self._detail,
                'date': self._date,
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = self.create_simple(data2)
        return movement1

    def create_simple_double(self, data):
        self.__validate_data(data)
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
        movement1 = self.create_simple(data1)
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
            movement2 = self.create_simple(data2)
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
        movement3 = self.create_simple(data3)

        return movement1

    def create_partner_movements(self, data):
        concept1 = Concept.objects.get(name='Aporte personal socio', concept_type=ConceptType.SIMPLEDOUBLE)
        data1 = {
            'box': self._partner.box,
            'concept': concept1,
            'movement_type': 'IN',
            'value': self._value,
            'detail': 'Aporte Inicial Socio',
            'date': datetime.now(),
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement1 = self.create_simple(data1)
        concept2 = Concept.objects.get(name='Aporte socio directo')
        if self._partner.partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=self._partner.office)
            data2 = {
                'box': box_don_juan,
                'concept': concept2,
                'movement_type': 'OUT',
                'value': int(self._value) * 2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(self._partner),
                'date': datetime.now(),
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = donjuan_manager.create_movement(data2)
        elif self._partner.partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=self._partner.direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': concept2,
                'movement_type': 'OUT',
                'value': int(self._value) * 2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(self._partner),
                'date': datetime.now(),
                'responsible': self._responsible,
                'ip': self._ip
            }
            movement2 = self.create_simple(data2)
        data3 = {
            'box': self._partner.box,
            'concept': concept2,
            'movement_type': 'IN',
            'value': int(self._value) * 2,
            'detail': 'Aporte Inicial Socio directo',
            'date': datetime.now(),
            'responsible': self._responsible,
            'ip': self._ip
        }
        movement3 = self.create_simple(data3)

        return movement1
