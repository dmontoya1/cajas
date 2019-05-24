
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.movement.models.movement_box_colombia import MovementBoxColombia
from cajas.movement.models.movement_don_juan import MovementDonJuan
from cajas.movement.models.movement_office import MovementOffice

from ..models.movement_box_colombia import MovementBoxColombia
from ..services.don_juan_usd_service import DonJuanUSDManager


class MovementBoxColombiaManager(object):

    def create_box_colombia_movement(self, data):
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        concept = get_object_or_404(Concept, pk=data['concept'])
        movement_colombia = self.create_colombia_movement(data)
        if concept == transfer_concept:
            if data['movement_type'] == MovementBoxColombia.IN:
                data['movement_type'] = MovementBoxColombia.OUT
            else:
                data['movement_type'] = MovementBoxColombia.IN
            if data['destine_box'] == 'CAJA_DON_JUAN':
                movement = MovementDonJuan.objects.create(
                    box_don_juan=get_object_or_404(BoxDonJuan, office=data['office']),
                    concept=concept,
                    movement_type=data['movement_type'],
                    value=data['value'],
                    detail=data['detail'],
                    date=data['date'],
                    responsible=data['responsible'],
                    ip=data['ip']
                )
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=data['office']),
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_OFICINA':
                movement = MovementOffice.objects.create(
                    box_office=data['office'].box,
                    concept=concept,
                    movement_type=data['movement_type'],
                    value=data['value'],
                    detail=data['detail'],
                    date=data['date'],
                    responsible=data['responsible'],
                    ip=data['ip'],
                )
            elif data['destine_box'] == 'CAJA_BANCO':
                self.create_bank_colombia_movement(data)
        return movement_colombia

    def create_colombia_movement(self, data):
        try:
            movement = MovementBoxColombia.objects.create(
                box_office=BoxColombia.objects.get(name='Caja Colombia'),
                concept=get_object_or_404(Concept, pk=data['concept'].pk),
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=data['responsible'],
                ip=data['ip'],
            )
        except:
            movement = MovementBoxColombia.objects.create(
                box_office=BoxColombia.objects.get(name='Caja Colombia'),
                concept=get_object_or_404(Concept, pk=data['concept']),
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=data['responsible'],
                ip=data['ip'],
            )
        return movement

    def create_box_bank_colombia_movement(self, data):
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        concept = get_object_or_404(Concept, pk=data['concept'])
        self.create_bank_colombia_movement(data)
        if concept == transfer_concept:
            if data['movement_type'] == MovementBoxColombia.IN:
                data['movement_type'] = MovementBoxColombia.OUT
            else:
                data['movement_type'] = MovementBoxColombia.IN
            if data['destine_box'] == 'CAJA_DON_JUAN':
                movement = MovementDonJuan.objects.create(
                    box_don_juan=get_object_or_404(BoxDonJuan, office=data['office']),
                    concept=concept,
                    movement_type=data['movement_type'],
                    value=data['value'],
                    detail=data['detail'],
                    date=data['date'],
                    responsible=data['responsible'],
                    ip=data['ip']
                )
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuan, office=data['office']),
                if data['movement_type'] == MovementBoxColombia.IN:
                    data['movement_type'] = MovementBoxColombia.OUT
                else:
                    data['movement_type'] = MovementBoxColombia.IN
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                self.create_colombia_movement(data)
            elif data['destine_box'] == 'CAJA_OFICINA':
                movement = MovementOffice.objects.create(
                    box_office=data['office'].box,
                    concept=concept,
                    movement_type=data['movement_type'],
                    value=data['value'],
                    detail=data['detail'],
                    date=data['date'],
                    responsible=data['responsible'],
                    ip=data['ip'],
                )

    def create_bank_colombia_movement(self, data):
        movement = MovementBoxColombia.objects.create(
            box_office=BoxColombia.objects.get(name="Caja Banco"),
            concept=get_object_or_404(Concept, pk=data['concept']),
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
        )
        return movement

    def __get_movement_by_pk(self, pk):
        return MovementBoxColombia.objects.filter(pk=pk)

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
