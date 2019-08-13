from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.boxes.models.box_office import BoxOffice
from cajas.concepts.models.concepts import Concept, ConceptType

from ..models import MovementBoxColombia, MovementDonJuan, MovementOffice
from ..services.don_juan_usd_service import DonJuanUSDManager
from .utils import update_movement_balance_on_create, delete_movement_by_box, get_last_movement, \
    update_all_movements_balance_on_create, update_all_movement_balance_on_update, update_movement_type_value, \
    update_movement_balance


class MovementBoxColombiaManager(object):

    def create_box_colombia_movement(self, data):
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        try:
            concept = get_object_or_404(Concept, pk=data['concept'])
            data['concept'] = concept
        except:
            data['concept'] = data['concept']
        movement_colombia = self.create_movement_box_colombia(data)
        if concept == transfer_concept:
            if data['movement_type'] == MovementBoxColombia.IN:
                data['movement_type'] = MovementBoxColombia.OUT
            else:
                data['movement_type'] = MovementBoxColombia.IN
            if data['destine_box'] == 'CAJA_DON_JUAN':
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
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=data['office']),
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_OFICINA':
                last_movement = get_last_movement(MovementOffice, 'box_office', data['box_office'], data['date'])
                if type(data['box_office'] is not BoxOffice):
                    data['box_office'] = BoxOffice.objects.get(pk=data['box_office'])
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
            elif data['destine_box'] == 'CAJA_BANCO':
                self.create_bank_colombia_movement(data)
        return movement_colombia

    def create_movement_box_colombia(self, data):
        box = BoxColombia.objects.get(name='Caja Colombia')
        last_movement = get_last_movement(MovementBoxColombia, 'box_office', box, data['date'])
        try:
            movement = MovementBoxColombia.objects.create(
                box_office=box,
                concept=data['concept'],
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=data['responsible'],
                ip=data['ip'],
            )
        except:
            movement = MovementBoxColombia.objects.create(
                box_office=box,
                concept=get_object_or_404(Concept, pk=data['concept']),
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=data['responsible'],
                ip=data['ip'],
            )
        update_movement_balance_on_create(last_movement, movement)
        update_all_movements_balance_on_create(
            MovementBoxColombia,
            'box_office',
            box,
            data['date'],
            movement
        )
        return movement

    def create_box_bank_colombia_movement(self, data):
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        concept = get_object_or_404(Concept, pk=data['concept'])
        try:
            concept = get_object_or_404(Concept, pk=data['concept'])
            data['concept'] = concept
        except:
            data['concept'] = data['concept']
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
                self.create_movement_box_colombia(data)
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
        box = BoxColombia.objects.get(name="Caja Banco")
        last_movement = get_last_movement(MovementBoxColombia, 'box_office', box, data['date'])
        movement = MovementBoxColombia.objects.create(
            box_office=box,
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
            MovementBoxColombia,
            'box_office',
            box,
            data['date'],
            movement
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
            current_movement = update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if self.__is_movement_value_updated(current_movement, data['value']):
            current_movement = update_movement_balance(current_movement, data['value'])
        current_movement_office.update(**object_data)
        update_all_movement_balance_on_update(
            MovementBoxColombia,
            'box_office',
            current_movement.box_office,
            current_movement.date,
            current_movement.pk,
            current_movement
        )

    def delete_box_colombia_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        delete_movement_by_box(current_movement, current_movement.box_office, MovementBoxColombia, 'box_office')
