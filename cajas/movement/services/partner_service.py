
from datetime import datetime

from django.db.models import Sum

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import PartnerType
from cajas.concepts.models.concepts import Concept, ConceptType, CrossoverType, Relationship

from ..models.movement_partner import MovementPartner
from ..services.don_juan_service import DonJuanManager
from ..services.office_service import MovementOfficeManager
from .utils import update_movement_balance_on_create, delete_movement_by_box, get_last_movement, \
    update_all_movements_balance_on_create, update_all_movement_balance_on_update, update_movement_type_value, \
    update_movement_balance, update_movement_balance_full_box

donjuan_manager = DonJuanManager()


class MovementPartnerManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_simple(self, data):
        self.__validate_data(data)
        last_movement = get_last_movement(MovementPartner, 'box_partner', data['box'], data['date'])
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
        update_movement_balance_on_create(last_movement, movement)
        update_all_movements_balance_on_create(
            MovementPartner,
            'box_partner',
            data['box'],
            data['date'],
            movement
        )
        return movement

    def create_double(self, data):
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
        if data['concept'].relationship == Relationship.OFFICE or \
           data['concept'].crossover_type == CrossoverType.OFFICE:
            office_manager = MovementOfficeManager()
            data['box_office'] = data['partner'].office.box
            data['movement_type'] = contrapart
            office_manager.create_movement(data)
        else:
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
                donjuan_manager.create_movement(data2)
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
                self.create_simple(data2)
        return movement1

    def create_simple_double(self, data):
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
        data2 = {
            'concept': concept2,
            'movement_type': 'OUT',
            'value': int(data['value']) * 2,
            'detail': 'Salida Aporte Nuevo socio {}'.format(data['partner']),
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2['box'] = box_don_juan
            donjuan_manager.create_movement(data2)
        elif data['partner'].partner_type == PartnerType.INDIRECTO:
            box_direct_partner = BoxPartner.objects.get(partner=data['partner'].direct_partner)
            data2['box'] = box_direct_partner
            self.create_simple(data2)
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

    def create_withdraw_movement(self, data):
        concept = Concept.objects.get(name='Retiro de Socio', concept_type=ConceptType.DOUBLE)
        data1 = {
            'box': data['box'],
            'concept': concept,
            'movement_type': 'OUT',
            'value': int(data['value']) * 3,
            'detail': data['detail'],
            'date': data['date'],
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement1 = self.create_simple(data1)
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2 = {
                'box': box_don_juan,
                'concept': concept.counterpart,
                'movement_type': 'IN',
                'value': int(data['value']) * 2,
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
                'concept': concept.counterpart,
                'movement_type': 'IN',
                'value': int(data['value']) * 2,
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = self.create_simple(data2)
        return movement1

    def create_withdraw_movement_full(self, data):
        concept = Concept.objects.get(name='Retiro de Socio', concept_type=ConceptType.DOUBLE)
        data1 = {
            'box': data['box'],
            'concept': concept,
            'movement_type': 'OUT',
            'value': int(data['value']) * 3,
            'detail': data['detail'],
            'date': data['date'],
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        movement1 = self.create_simple(data1)
        if data['partner'].partner_type == PartnerType.DIRECTO:
            box_don_juan = BoxDonJuan.objects.get(office=data['partner'].office)
            data2 = {
                'box': box_don_juan,
                'concept': concept.counterpart,
                'movement_type': 'IN',
                'value': int(data['value']) * 3,
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
                'concept': concept.counterpart,
                'movement_type': 'IN',
                'value': int(data['value']) * 3,
                'detail': data['detail'],
                'date': data['date'],
                'responsible': data['responsible'],
                'ip': data['ip']
            }
            movement2 = self.create_simple(data2)
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

    def __get_movement_by_pk(self, pk):
        return MovementPartner.objects.filter(pk=pk)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def __is_date_updated(self, movement, new_date):
        return movement.date != new_date

    def __is_movement_date_update(self, movement, new_date):
        return movement.date != new_date

    def update_partner_movement(self, data):
        current_movement_partner = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_partner.first()
        current_concept = self.__get_current_concept(data['concept'])
        object_data = dict()
        object_data['box_partner'] = current_movement.box_partner
        object_data['concept'] = current_concept
        object_data['value'] = data['value']
        object_data['movement_type'] = data['movement_type']
        object_data['detail'] = data['detail']
        object_data['date'] = data['date']
        data['movement'] = current_movement
        data['box'] = current_movement.box_partner
        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            current_movement = update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if self.__is_movement_value_updated(current_movement, data['value']):
            current_movement = update_movement_balance(current_movement, data['value'])
        current_movement_partner.update(**object_data)
        update_all_movement_balance_on_update(
            MovementPartner,
            'box_partner',
            current_movement.box_partner,
            current_movement.date,
            current_movement.pk,
            current_movement
        )
        if self.__is_movement_date_update(current_movement, data['date']):
            first_movement = MovementPartner.objects.filter(box_partner=current_movement.box_partner).last()
            update_movement_balance_full_box(
                MovementPartner,
                'box_partner',
                current_movement.box_partner,
                first_movement.date,
                first_movement
            )

    def delete_partner_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        delete_movement_by_box(current_movement, current_movement.box_partner, MovementPartner, 'box_partner')
