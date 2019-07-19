
from cajas.concepts.models.concepts import Concept

from ..models.movement_don_juan_usd import MovementDonJuanUsd
from .utils import update_movement_balance_on_create, delete_movement_by_box, get_last_movement, \
    update_all_movements_balance_on_create, update_all_movement_balance_on_update, update_movement_type_value, \
    update_movement_balance


class DonJuanUSDManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_movement(self, data):
        self.__validate_data(data)
        last_movement = get_last_movement(MovementDonJuanUsd, 'box_don_juan', data['box'], data['date'])
        movement = MovementDonJuanUsd.objects.create(
            box_don_juan=data['box'],
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
            MovementDonJuanUsd,
            'box_don_juan',
            data['box'],
            data['date'],
            movement
        )
        return movement

    def __get_movement_by_pk(self, pk):
        return MovementDonJuanUsd.objects.filter(pk=pk)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def update_don_juan_movement(self, data):
        current_don_juan_movement = self.__get_movement_by_pk(data['pk'])
        current_movement = current_don_juan_movement.first()
        current_concept = self.__get_current_concept(data['concept'])
        object_data = dict()
        object_data['box_don_juan'] = current_movement.box_don_juan
        object_data['concept'] = current_concept
        object_data['value'] = data['value']
        object_data['movement_type'] = data['movement_type']
        object_data['detail'] = data['detail']
        object_data['date'] = data['date']
        data['movement'] = current_movement
        data['box'] = current_movement.box_don_juan

        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            current_movement = update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if self.__is_movement_value_updated(current_movement, data['value']):
            current_movement = update_movement_balance(current_movement, data['value'])
        current_don_juan_movement.update(**object_data)
        update_all_movement_balance_on_update(
            MovementDonJuanUsd,
            'box_don_juan',
            current_movement.box_don_juan,
            current_movement.date,
            current_movement.pk,
            current_movement
        )

    def delete_don_juan_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        delete_movement_by_box(current_movement, current_movement.box_don_juan, MovementDonJuanUsd, 'box_don_juan')
