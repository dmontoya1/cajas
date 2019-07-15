
from datetime import datetime

from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_partner import BoxPartner
from cajas.concepts.models.concepts import Concept
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.office.models.officeCountry import OfficeCountry

from ..models.partner import Partner


class PartnerManager(object):

    PROPERTIES = ['user', 'office', 'partner_type', 'direct_partner', ]

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_partner(self, data):
        self.__validate_data(data)
        partner = Partner.objects.create(
            user=data['user'],
            office=data['office'],
            partner_type=data['partner_type'],
            direct_partner=data['direct_partner'],
        )
        return partner

    def __cleaning_partner_box(self, data):
        movement_partner_manager = MovementPartnerManager()
        if data['last_balance'] > 0:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        else:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        data = {
            'box': data['box'],
            'concept': concept,
            'movement_type': movement_type,
            'value': abs(data['last_balance']),
            'detail': 'Migracion de socio',
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        partner_movement = movement_partner_manager.create_simple(data)

    def __add_don_juan_movement(self, data):
        movement_don_juan_manager = DonJuanManager()
        box_don_juan = get_object_or_404(BoxDonJuan, office=data['partner'].office)
        if data['last_balance'] > 0:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        else:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        data = {
            'box': box_don_juan,
            'concept': concept,
            'movement_type': movement_type,
            'value': abs(data['last_balance']),
            'detail': 'Migracion de socio: {}'.format(data['partner']),
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        don_juan_movement = movement_don_juan_manager.create_movement(data)

    def __add_new_partner_box_balance(self, data):
        movement_partner_manager = MovementPartnerManager()
        if data['last_balance'] > 0:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        else:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        data = {
            'box': data['new_partner'].box,
            'concept': concept,
            'movement_type': movement_type,
            'value': abs(data['last_balance']),
            'detail': 'Migracion de socio',
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        partner_movement = movement_partner_manager.create_simple(data)

    def __add_new_don_juan_movement(self, data):
        movement_don_juan_manager = DonJuanManager()
        box_don_juan = get_object_or_404(BoxDonJuan, office=data['new_partner'].office)
        if data['last_balance'] > 0:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        else:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        data = {
            'box': box_don_juan,
            'concept': concept,
            'movement_type': movement_type,
            'value': abs(data['last_balance']),
            'detail': 'Migracion de socio: {}'.format(data['new_partner']),
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        don_juan_movement = movement_don_juan_manager.create_movement(data)

    def __inactive_old_partner(self, data):
        data['partner'].is_active = False
        data['partner'].save()
        data['box'].is_active = False
        data['box'].save()

    def migrate_partner(self, data):
        target_office = get_object_or_404(OfficeCountry, pk=data['office'])
        for i in data.getlist("partners[]"):
            partner = get_object_or_404(Partner, pk=i)
            data['partner'] = partner
            data['box'] = partner.box
            data['last_balance'] = partner.box.balance
            self.__cleaning_partner_box(data)
            self.__add_don_juan_movement(data)
            data_partner = {
                'user': partner.user,
                'office': target_office,
                'partner_type': partner.partner_type,
                'direct_partner': partner.direct_partner
            }
            new_partner = self.create_partner(data_partner)
            data['new_partner'] = new_partner
            self.__add_new_partner_box_balance(data)
            self.__add_new_don_juan_movement(data)
            self.__inactive_old_partner(data)
