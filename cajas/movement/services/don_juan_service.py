
from cajas.concepts.models.concepts import Concept

from ..models import MovementDonJuan, MovementOffice, MovementDonJuanUsd, MovementBoxColombia
from .utils import update_movements_balance, update_movement_balance_on_create, delete_movement_by_box, \
    get_last_movement, update_all_movements_balance_on_create, update_movement_type_value, \
    update_movement_balance, update_movement_balance_full_box


class DonJuanManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_movement(self, data):
        self.__validate_data(data)
        last_movement = get_last_movement(MovementDonJuan, 'box_don_juan', data['box'], data['date'])
        try:
            movement = MovementDonJuan.objects.create(
                box_don_juan=data['box'][0],
                concept=data['concept'],
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=data['responsible'],
                ip=data['ip']
            )
        except Exception as e:
            print("EXCEPTION", e)
            movement = MovementDonJuan.objects.create(
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
            MovementDonJuan,
            'box_don_juan',
            data['box'],
            data['date'],
            movement
        )
        return movement

    def __get_movement_by_pk(self, pk):
        return MovementDonJuan.objects.filter(pk=pk)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def __update_value(self, data):
        current_movement = data['movement']
        update_movement_balance(current_movement, data['value'])
        if current_movement.movement_office:
            movement_office = MovementOffice.objects.get(pk=current_movement.movement_office)
            update_movement_balance(
                movement_office,
                data['value']
            )
            self.update_movement_value(movement_office, data['value'])
            first_movement = MovementOffice.objects.filter(
                box_office=movement_office.box_office
            ).last()
            update_movement_balance_full_box(
                MovementOffice,
                'box_office',
                movement_office.box_office,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_don_juan_usd:
            movement_don_juan_usd = MovementDonJuanUsd.objects.get(pk=current_movement.movement_don_juan_usd)
            update_movement_balance(
                movement_don_juan_usd,
                data['value']
            )
            self.update_movement_value(movement_don_juan_usd, data['value'])
            first_movement = MovementDonJuanUsd.objects.filter(
                box_don_juan=movement_don_juan_usd.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuanUsd,
                'box_don_juan',
                movement_don_juan_usd.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_box_colombia:
            movement_box_colombia = MovementBoxColombia.objects.get(pk=current_movement.movement_box_colombia)
            update_movement_balance(
                movement_box_colombia,
                data['value']
            )
            self.update_movement_value(movement_box_colombia, data['value'])
            first_movement = MovementBoxColombia.objects.filter(
                box_office=movement_box_colombia.box_office
            ).last()
            update_movement_balance_full_box(
                MovementBoxColombia,
                'box_office',
                movement_box_colombia.box_office,
                first_movement.date,
                first_movement
            )

    def update_movement_value(self, movement, value):
        movement.value = value
        movement.save()

    def __update_movement_type(self, data):
        current_movement = data['movement']
        update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if current_movement.movement_office:
            movement_office = MovementOffice.objects.get(pk=current_movement.movement_office)
            self.update_counterpart_movement_type(movement_office)
            first_movement = MovementOffice.objects.filter(
                box_office=movement_office.box_office
            ).last()
            update_movement_balance_full_box(
                MovementOffice,
                'box_office',
                movement_office.box_office,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_don_juan_usd:
            movement_don_juan_usd = MovementDonJuanUsd.objects.get(pk=current_movement.movement_don_juan_usd)
            self.update_counterpart_movement_type(movement_don_juan_usd)
            first_movement = MovementDonJuanUsd.objects.filter(
                box_don_juan=movement_don_juan_usd.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuanUsd,
                'box_don_juan',
                movement_don_juan_usd.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_box_colombia:
            movement_box_colombia = MovementBoxColombia.objects.get(pk=current_movement.movement_box_colombia)
            self.update_counterpart_movement_type(movement_box_colombia)
            first_movement = MovementBoxColombia.objects.filter(
                box_office=movement_box_colombia.box_office
            ).last()
            update_movement_balance_full_box(
                MovementBoxColombia,
                'box_office',
                movement_box_colombia.box_office,
                first_movement.date,
                first_movement
            )

    def update_counterpart_movement_type(self, movement):
        if movement.movement_type == 'IN':
            movement.movement_type = 'OUT'
        else:
            movement.movement_type = 'IN'
        movement.save()

    def __delete_related_movement(self, movement):
        if movement.movement_office:
            movement_office = MovementOffice.objects.get(pk=movement.movement_office)
            delete_movement_by_box(
                movement_office,
                movement_office.box_office,
                MovementOffice,
                'box_office'
            )
        if movement.movement_don_juan_usd:
            movement_don_juan_usd = MovementDonJuanUsd.objects.get(pk=movement.movement_don_juan_usd)
            delete_movement_by_box(
                movement_don_juan_usd,
                movement_don_juan_usd.box_don_juan,
                MovementDonJuanUsd,
                'box_don_juan_usd'
            )
        if movement.movement_box_colombia:
            movement_box_colombia = MovementBoxColombia.objects.get(pk=movement.movement_box_colombia)
            delete_movement_by_box(
                movement_box_colombia,
                movement_box_colombia.box_office,
                MovementBoxColombia,
                'box_office'
            )

    def __is_movement_date_update(self, movement, new_date):
        return movement.date != new_date

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
            self.__update_movement_type(data)
        if self.__is_movement_value_updated(current_movement, data['value']):
            self.__update_value(data)
        current_don_juan_movement.update(**object_data)
        all_movements = current_movement.box_don_juan.movements.order_by('date', 'pk')
        update_movements_balance(
            all_movements,
            0,
            current_movement.box_don_juan
        )
        if self.__is_movement_date_update(current_movement, data['date']):
            all_movements = current_movement.box_don_juan.movements.order_by('date', 'pk')
            update_movements_balance(
                all_movements,
                0,
                current_movement.box_don_juan
            )
        return current_don_juan_movement.first()

    def delete_don_juan_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        self.__delete_related_movement(current_movement)
        delete_movement_by_box(current_movement, current_movement.box_don_juan, MovementDonJuan, 'box_don_juan')
