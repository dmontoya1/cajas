
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept, ConceptType

from ..models.movement_office import MovementOffice
from ..services.don_juan_service import DonJuanManager
from ..services.don_juan_usd_service import DonJuanUSDManager
from ..services.box_colombia_service import MovementBoxColombiaManager


class MovementOfficeManager(object):

    PROPERTIES = ['box_office', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

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
                data['box'] = get_object_or_404(BoxDonJuan, office=data['office']),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=data['office']),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Colombia"),
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                box_colombia_manager.create_colombia_movement(data)
            elif data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Banco"),
                if data['movement_type'] == 'IN':
                    data['movement_type'] = 'OUT'
                else:
                    data['movement_type'] = 'IN'
                box_colombia_manager.create_bank_colombia_movement(data)

    def create_movement(self, data):
        self.__validate_data(data)
        movement = MovementOffice.objects.create(
            box_office=data['office'].box,
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
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

    def __update_movement_type(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance += (int(data['movement'].value) * 2)
        else:
            box.balance -= (int(data['movement'].value) * 2)
        box.save()

    def __update_value(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance -= int(data['movement'].value)
            box.balance += int(data['value'])
        else:
            box.balance += int(data['movement'].value)
            box.balance -= int(data['value'])
        box.save()

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
            self.__update_movement_type(data)
        if self.__is_movement_value_updated(current_movement, data['value']):
            self.__update_value(data)
        current_movement_office.update(**object_data)
