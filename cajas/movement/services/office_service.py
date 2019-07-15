
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept, ConceptType

from ..models.movement_office import MovementOffice
from ..services.don_juan_service import DonJuanManager
from ..services.don_juan_usd_service import DonJuanUSDManager
from ..services.box_colombia_service import MovementBoxColombiaManager
from .utils import update_movements_balance, get_next_related_movement_by_date_and_pk, \
    update_movement_balance_on_create, delete_movement_by_box, get_last_movement, \
    update_all_movements_balance_on_create, update_all_movement_balance_on_update, update_movement_type_value, \
    update_movement_balance


class MovementOfficeManager(object):

    PROPERTIES = ['box_office', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_office_movement(self, data):
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        concept = get_object_or_404(Concept, pk=data['concept'])
        data['concept'] = concept
        self.create_movement(data)
        if concept == transfer_concept:
            if data['destine_box'] == 'CAJA_DON_JUAN':
                don_juan_manager = DonJuanManager()
                data['box'] = BoxDonJuan.objects.get(office=data['office']),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = BoxDonJuanUSD.objects.get(office=data['office']),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = BoxColombia.objects.get(name="Caja Colombia"),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                box_colombia_manager.create_colombia_movement(data)
            elif data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = BoxColombia.objects.get(name="Caja Banco"),
                if data['movement_type'] == 'IN':
                    data['movement_type'] = 'OUT'
                else:
                    data['movement_type'] = 'IN'
                box_colombia_manager.create_bank_colombia_movement(data)

    def create_movement(self, data):
        self.__validate_data(data)
        last_movement = get_last_movement(MovementOffice, 'box_office', data['box_office'], data['date'])
        movement = MovementOffice.objects.create(
            box_office=data['box_office'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
        )
        update_movement_balance_on_create(last_movement, movement)
        update_all_movements_balance_on_create(
            MovementOffice,
            'box_office',
            data['box_office'],
            data['date'],
            movement
        )
        return movement

    def __get_movement_by_pk(self, pk):
        return MovementOffice.objects.filter(pk=pk)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def update_office_movement(self, data):
        current_movement_office = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_office.first()
        current_concept = self.__get_current_concept(data['concept'])
        object_data = dict()
        object_data['box_office'] = current_movement.box_office
        object_data['concept'] = current_concept
        object_data['value'] = data['value']
        object_data['movement_type'] = data['movement_type']
        object_data['detail'] = data['detail']
        object_data['date'] = data['date']
        data['movement'] = current_movement
        data['box'] = current_movement.box_office
        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if self.__is_movement_value_updated(current_movement, data['value']):
            update_movement_balance(current_movement, data['value'])
        current_movement_office.update(**object_data)
        update_all_movement_balance_on_update(
            MovementOffice,
            'box_office',
            current_movement.box_office,
            current_movement.date,
            current_movement.pk,
            current_movement
        )

    def delete_office_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        delete_movement_by_box(current_movement, current_movement.box_office, MovementOffice, 'box_office')
