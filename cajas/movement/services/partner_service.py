
from datetime import datetime

from django.db.models import Sum

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
        if data['movement_type'] == 'IN':
            contrapart = 'OUT'
        else:
            contrapart = 'IN'
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2 = {
                'box': box_don_juan,
                'concept': data['concept'].counterpart,
                'movement_type': contrapart,
                'value': data['value'],
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = donjuan_manager.create_movement(data2)
        elif data['partner'].partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=data['partner'].direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': data['concept'].counterpart,
                'movement_type': contrapart,
                'value': data['value'],
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = self.create_simple(data2)
        return movement1

    def create_simple_double(self, data):
        self.__validate_data(data)
        data1 = {
            'box': data['partner'].box,
            'concept': data['concept'],
            'movement-type': data['movement_type'],
            'value': data['value'],
            'detail': data['detail'],
            'date': data['date'],
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement1 = self.create_simple(data1)
        if data['movement_type'] == 'IN':
            contrapart = 'OUT'
        else:
            contrapart = 'IN'
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2 = {
                'box': box_don_juan,
                'concept': data['concept'],
                'movement_type': contrapart,
                'value': data['value'],
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = donjuan_manager.create_movement(data2)
        elif data['partner'].partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=data['partner'].direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': data['concept'],
                'movement-type': contrapart,
                'value': data['value'],
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = self.create_simple(data2)
        data3 = {
            'box': data['partner'].box,
            'concept': data['concept'],
            'movement-type': contrapart,
            'value': data['value'],
            'detail': data['detail'],
            'date': data['date'],
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement3 = self.create_simple(data3)

        return movement1

    def create_partner_movements(self, data):
        concept1 = Concept.objects.get(name='Aporte personal socio', concept_type=ConceptType.SIMPLEDOUBLE)
        data1 = {
            'box': data['partner'].box,
            'concept': concept1,
            'movement_type': 'IN',
            'value': data['value'],
            'detail': 'Aporte Inicial Socio',
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement1 = self.create_simple(data1)
        concept2 = Concept.objects.get(name='Aporte socio directo')
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2 = {
                'box': box_don_juan,
                'concept': concept2,
                'movement_type': 'OUT',
                'value': int(data['value']) * 2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(data['partner']),
                'date': datetime.now(),
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = donjuan_manager.create_movement(data2)
        elif data['partner'].partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=data['partner'].direct_partner)
            data2 = {
                'box': box_direct_partner,
                'concept': concept2,
                'movement_type': 'OUT',
                'value': int(data['value']) * 2,
                'detail': 'Salida Aporte Nuevo socio {}'.format(data['partner']),
                'date': datetime.now(),
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = self.create_simple(data2)
        data3 = {
            'box': data['partner'].box,
            'concept': concept2,
            'movement_type': 'IN',
            'value': int(data['value']) * 2,
            'detail': 'Aporte Inicial Socio directo',
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement3 = self.create_simple(data3)

        return movement1

    def get_user_value(self, data):
        month = datetime.now().month
        total = MovementPartner.objects.filter(
            box_partner=data['box'],
            concept=data['concept'],
            movement_type='OUT',
            date__month=month,
        ).aggregate(Sum('value'))
        if total['value__sum'] is None:
            total['value__sum'] = 0
        return total
