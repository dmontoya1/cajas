
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.inventory.models.category import Category
from cajas.inventory.models.brand import Brand
from cajas.office.services.office_item_create import OfficeItemsManager

from ..models import MovementDonJuan, MovementOffice, MovementDonJuanUsd, MovementBoxColombia
from ..services.don_juan_service import DonJuanManager
from ..services.don_juan_usd_service import DonJuanUSDManager
from ..services.box_colombia_service import MovementBoxColombiaManager
from .utils import update_movements_balance, update_movement_balance_on_create, delete_movement_by_box, \
    get_last_movement, update_all_movements_balance_on_create, update_movement_type_value, \
    update_movement_balance, update_movement_balance_full_box


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
        movement = self.create_movement(data)
        if concept == transfer_concept:
            data['concept'] = concept.counterpart
            if data['destine_box'] == 'CAJA_DON_JUAN':
                don_juan_manager = DonJuanManager()
                data['box'] = BoxDonJuan.objects.get(office=data['office'])
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_movement = don_juan_manager.create_movement(data)
                movement.movement_don_juan = don_juan_movement.pk
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = BoxDonJuanUSD.objects.get(office=data['office'])
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                don_juan_usd_movement = don_juan_usd_manager.create_movement(data)
                movement.movement_don_juan_usd = don_juan_usd_movement.pk
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = BoxColombia.objects.get(name="Caja Colombia")
                if data['movement_type'] == MovementOffice.IN:
                    data['movement_type'] = MovementOffice.OUT
                else:
                    data['movement_type'] = MovementOffice.IN
                movement_box_colombia = box_colombia_manager.create_movement_box_colombia(data)
                movement.movement_box_colombia = movement_box_colombia.pk
            elif data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = BoxColombia.objects.get(name="Caja Banco")
                if data['movement_type'] == 'IN':
                    data['movement_type'] = 'OUT'
                else:
                    data['movement_type'] = 'IN'
                movement_box_bank_colombia = box_colombia_manager.create_bank_colombia_movement(data)
                movement.movement_box_colombia = movement_box_bank_colombia.pk
            movement.save()
        if "brand" in data:
            data["brand"] = get_object_or_404(Brand, pk=data["brand"])
            data["category"] = get_object_or_404(Category, pk=data["category"])
            office_items_manager = OfficeItemsManager()
            office_items_manager.create_office_item(data)

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
                movement_box_colombia,
                first_movement.date,
                first_movement
            )

    def update_movement_value(self, movement, value):
        movement.value = value
        movement.save()

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

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

    def __is_date_updated(self, movement, new_date):
        return movement.date != new_date

    def __delete_related_movement(self, movement):
        if movement.movement_don_juan:
            movement_don_juan = MovementDonJuan.objects.get(pk=movement.movement_don_juan)
            delete_movement_by_box(
                movement_don_juan,
                movement_don_juan.box_don_juan,
                MovementDonJuan,
                'box_don_juan'
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

    def delete_office_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        self.__delete_related_movement(current_movement)
        delete_movement_by_box(current_movement, current_movement.box_office, MovementOffice, 'box_office')
