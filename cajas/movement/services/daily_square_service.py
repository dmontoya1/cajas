
from datetime import datetime

from django.db.models import Sum

from concepts.models.concepts import Concept
from cajas.users.models.user import User
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit
from concepts.services.stop_service import StopManager
from ..models.movement_daily_square import MovementDailySquare

from webclient.views.utils import get_object_or_none


class MovementDailySquareManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip',
                  'unit', 'user', 'office', 'loan', 'chain']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_movement(self, data):
        self.__validate_data(data)
        movement = MovementDailySquare.objects.create(
            box_daily_square=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
            unit=data['unit'],
            user=data['user'],
            office=data['office'],
        )
        return movement

    def create_new_partner_movement(self, data):
        movement = MovementDailySquare.objects.create(
            box_daily_square=data['box'],
            concept=Concept.objects.get(name='Aporte personal socio'),
            movement_type='IN',
            value=data['value'],
            detail='Aporte personal {}'.format(data['partner']),
            date=datetime.now(),
            responsible=data['responsible'],
            ip=data['ip'],
        )
        return movement

    def get_user_value(self, data):
        month = datetime.now().month
        total = MovementDailySquare.objects.filter(
            box_daily_square=data['box'],
            concept=data['concept'],
            movement_type='OUT',
            date__month=month,
        ).aggregate(Sum('value'))
        if total['value__sum'] is None:
            total['value__sum'] = 0
        return total

    def get_out_movement_current_value_by_box_and_concept(self, box, concept):
        month = datetime.now().month
        total = MovementDailySquare.objects.filter(
            box_daily_square=box,
            concept=concept,
            movement_type='OUT',
            date__month=month,
        ).aggregate(Sum('value'))
        if total['value__sum'] is None:
            total['value__sum'] = 0
        return total

    def __get_movement_by_pk(self, pk):
        return MovementDailySquare.objects.get(pk=pk)

    def __get_user_box_daily_square(self, user_id, office_slug):
        return BoxDailySquare.objects.get(user__pk=user_id, office__slug=office_slug)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def __update_movement_type(self, data):
        update_mvment = data['movement']
        self.update_movement(data)
        if update_mvment.movement_don_juan:
            data['box'] = update_mvment.movement_don_juan.box_don_juan
            self.update_movement(data)
        if update_mvment.movement_don_juan_usd:
            data['box'] = update_mvment.movement_don_juan_usd.box_don_juan
            self.update_movement(data)
        if update_mvment.movement_partner:
            data['box'] = update_mvment.movement_partner.box_partner
            self.update_movement(data)
        if update_mvment.movement_office:
            data['box'] = update_mvment.movement_office.box_office
            self.update_movement(data)
        if update_mvment.movement_cd:
            data['box'] = update_mvment.movement_cd.box_daily_square
            self.update_movement(data)


    def update_value(self, data):
        update_mvment = data['movement']
        self.update_extern_value(data)
        if update_mvment.movement_don_juan:
            data['box'] = update_mvment.movement_don_juan.box_don_juan
            self.update_extern_value(data)
            update_mvment.movement_don_juan.value = data['value']
            update_mvment.movement_don_juan.save()
        if update_mvment.movement_don_juan_usd:
            data['box'] = update_mvment.movement_don_juan_usd.box_don_juan
            self.update_extern_value(data)
            update_mvment.movement_don_juan_usd.value = data['value']
            update_mvment.movement_don_juan_usd.save()
        if update_mvment.movement_partner:
            data['box'] = update_mvment.movement_partner.box_partner
            self.update_extern_value(data)
            update_mvment.movement_partner.value = data['value']
            update_mvment.movement_partner.save()
        if update_mvment.movement_office:
            data['box'] = update_mvment.movement_office.box_office
            self.update_extern_value(data)
            update_mvment.movement_office.value = data['value']
            update_mvment.movement_office.save()
        if update_mvment.movement_cd:
            data['box'] = update_mvment.movement_cd.box_daily_square
            self.update_extern_value(data)
            update_mvment.movement_cd.value = data['value']
            update_mvment.movement_cd.save()

    def update_movement(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance = box.balance + (int(data['movement'].value) * 2)
        else:
            box.balance = box.balance - (int(data['movement'].value) * 2)
        box.save()

    def update_extern_value(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance -= int(data['movement'].value)
            box.balance += int(data['value'])
        else:
            box.balance += int(data['movement'].value)
            box.balance -= int(data['value'])
        box.save()

    def update_daily_square_movement(self, data):
        # validate data

        # get movement
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        # get box daily square
        current_user_box_daily_square = self.__get_user_box_daily_square(data['user_id'], data['office_slug'])
        # get current concept
        current_concept = self.__get_current_concept(data['concept'])

        current_user = get_object_or_none(User, pk=data.get('user', None))
        object_data = data.copy()
        object_data['user'] = current_user
        object_data['office'] = get_object_or_none(OfficeCountry, pk=data.get('office', None))
        object_data['unit'] = get_object_or_none(Unit, pk=data.get('unit', None))

        if self.__is_movement_type_updated(current_movement_daily_square, data['movement_type']):
            self.__update_movement_type(object_data)

        if self.__is_movement_value_updated(current_movement_daily_square, data['value']):
            self.update_value(object_data)

        if current_user is not None:
            stop_manager = StopManager(current_user)
            if stop_manager.user_has_tops_for_concept(current_concept):
                user_movements_top_value = stop_manager.get_user_movements_top_value_by_concept(current_concept)

                user_movements_current_value = self.get_out_movement_current_value_by_box_and_concept(
                    current_user_box_daily_square,
                    current_concept
                )
                if user_movements_top_value >= (user_movements_current_value + data['value']):
                    current_movement_daily_square.update(**object_data)
            else:
                raise Exception('user has exceed limit')
        else:
            current_movement_daily_square.update(**object_data)

