from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.boxes.models.box_office import BoxOffice
from cajas.concepts.models.concepts import Concept, ConceptType

from ..services.don_juan_usd_service import DonJuanUSDManager
from ..models import MovementDonJuan, MovementOffice, MovementDonJuanUsd, MovementBoxColombia
from .utils import update_movements_balance, update_movement_balance_on_create, delete_movement_by_box, \
    get_last_movement, update_all_movements_balance_on_create, update_movement_type_value, \
    update_movement_balance, update_movement_balance_full_box


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
            concept = data['concept']
        movement_colombia = self.create_movement_box_colombia(data)
        if concept == transfer_concept:
            data['concept'] = concept.counterpart
            if data['movement_type'] == MovementBoxColombia.IN:
                data['movement_type'] = MovementBoxColombia.OUT
            else:
                data['movement_type'] = MovementBoxColombia.IN
            if data['destine_box'] == 'CAJA_DON_JUAN':
                data['box'] = BoxDonJuan.objects.get(office=data['office'])
                last_movement = get_last_movement(MovementDonJuan, 'box_don_juan', data['box'], data['date'])
                try:
                    movement_don_juan = MovementDonJuan.objects.create(
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
                    movement_don_juan = MovementDonJuan.objects.create(
                        box_don_juan=data['box'],
                        concept=data['concept'],
                        movement_type=data['movement_type'],
                        value=data['value'],
                        detail=data['detail'],
                        date=data['date'],
                        responsible=data['responsible'],
                        ip=data['ip']
                    )
                update_movement_balance_on_create(last_movement, movement_don_juan)
                update_all_movements_balance_on_create(
                    MovementDonJuan,
                    'box_don_juan',
                    data['box'],
                    data['date'],
                    movement_don_juan
                )
                movement_colombia.movement_don_juan = movement_don_juan.pk
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=data['office'])
                data['value'] = data['value_usd']
                movement_usd = don_juan_usd_manager.create_movement(data)
                movement_colombia.movement_don_juan_usd = movement_usd.pk
            elif data['destine_box'] == 'CAJA_OFICINA':
                last_movement = get_last_movement(MovementOffice, 'box_office', data['box_office'], data['date'])
                if type(data['box_office']) is not BoxOffice:
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
                movement_colombia.movement_office = movement.pk
            elif data['destine_box'] == 'CAJA_BANCO':
                movement = self.create_bank_colombia_movement(data)
                movement_colombia.movement_box_colombia = movement.pk
            movement_colombia.save()
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
        try:
            concept = get_object_or_404(Concept, pk=data['concept'])
            data['concept'] = concept
        except:
            concept = data['concept']
        movement_colombia = self.create_bank_colombia_movement(data)
        if concept == transfer_concept:
            data['concept'] = concept.counterpart
            if data['movement_type'] == MovementBoxColombia.IN:
                data['movement_type'] = MovementBoxColombia.OUT
            else:
                data['movement_type'] = MovementBoxColombia.IN
            if data['destine_box'] == 'CAJA_DON_JUAN':
                data['box'] = BoxDonJuan.objects.get(office=data['office'])
                last_movement = get_last_movement(MovementDonJuan, 'box_don_juan', data['box'], data['date'])
                movement = MovementDonJuan.objects.create(
                    box_don_juan=get_object_or_404(BoxDonJuan, office=data['office']),
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
                movement_colombia.movement_don_juan = movement.pk
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuan, office=data['office']),
                if data['movement_type'] == MovementBoxColombia.IN:
                    data['movement_type'] = MovementBoxColombia.OUT
                else:
                    data['movement_type'] = MovementBoxColombia.IN
                movement_usd = don_juan_usd_manager.create_movement(data)
                movement_colombia.movement_don_juan_usd = movement_usd.pk
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                movement = self.create_movement_box_colombia(data)
                movement_colombia.movement_box_colombia = movement.pk
            elif data['destine_box'] == 'CAJA_OFICINA':
                last_movement = get_last_movement(MovementOffice, 'box_office', data['box_office'], data['date'])
                if type(data['box_office']) is not BoxOffice:
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
                movement_colombia.movement_office = movement.pk
            movement_colombia.save()
        return movement_colombia

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

    def __update_value(self, data):
        current_movement = data['movement']
        update_movement_balance(current_movement, data['value'])
        if current_movement.movement_don_juan:
            movement_don_juan = MovementDonJuan.objects.get(pk=current_movement.movement_don_juan)
            update_movement_balance(
                movement_don_juan,
                data['value']
            )
            self.update_movement_value(movement_don_juan, data['value'])
            first_movement = MovementDonJuan.objects.filter(
                box_don_juan=movement_don_juan.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuan,
                'box_don_juan',
                movement_don_juan.box_don_juan,
                first_movement.date,
                first_movement
            )
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
                data['value_usd']
            )
            self.update_movement_value(movement_don_juan_usd, data['value_usd'])
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
        if current_movement.movement_don_juan:
            movement_don_juan = MovementDonJuan.objects.get(pk=current_movement.movement_don_juan)
            self.update_counterpart_movement_type(movement_don_juan)
            first_movement = MovementDonJuan.objects.filter(
                box_don_juan=movement_don_juan.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuan,
                'box_don_juan',
                movement_don_juan.box_don_juan,
                first_movement.date,
                first_movement
            )
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
        if movement.movement_don_juan:
            movement_don_juan = MovementDonJuan.objects.get(pk=movement.movement_don_juan)
            delete_movement_by_box(
                movement_don_juan,
                movement_don_juan.box_don_juan,
                MovementDonJuan,
                'box_don_juan'
            )
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
                'box_don_juan'
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
        all_movements = current_movement.box_office.movements.order_by('date', 'pk')
        update_movements_balance(
            all_movements,
            0,
            current_movement.box_office
        )

    def delete_box_colombia_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        self.__delete_related_movement(current_movement)
        delete_movement_by_box(current_movement, current_movement.box_office, MovementBoxColombia, 'box_office')
