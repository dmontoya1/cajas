
from datetime import datetime

from django.shortcuts import get_object_or_404

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxPartner
from concepts.models.concepts import Concept
from movement.services.don_juan_service import DonJuanManager
from movement.services.partner_service import MovementPartnerManager
from office.models.officeCountry import OfficeCountry

from ..models.partner import Partner


class PartnerManager(object):

    PROPERTIES = ['user', 'office', 'partner_type', 'direct_partner', ]

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

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
        if data['box'].balance > 0:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        else:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        data = {
            'box': data['box'],
            'concept': concept,
            'movement_type': movement_type,
            'value': data['box'].balance,
            'detail': 'Migracion de socio',
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        partner_movement = movement_partner_manager.create_simple(data)

    def __add_don_juan_movement(self, data):
        movement_don_juan_manager = DonJuanManager()
        if data['box'].balance > 0:
            movement_type = 'IN'
            concept = get_object_or_404(Concept, name='Otros Ingresos')
        else:
            movement_type = 'OUT'
            concept = get_object_or_404(Concept, name='Otros Egresos')
        data = {
            'box': data['box_don_juan'],
            'concept': concept,
            'movement_type': movement_type,
            'value': data['box'].balance,
            'detail': 'Migracion de socio: {}'.format(data['partner']),
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        don_juan_movement = movement_don_juan_manager.create_movement(data)

    def migrate_partner(self, data):
        target_office = get_object_or_404(OfficeCountry, pk=data['office'])
        for i in data.getlist("partners[]"):
            partner = get_object_or_404(Partner, pk=i)
            data['partner'] = partner
            data['box'] = partner.box
            self.__cleaning_partner_box(data)
            data['box_don_juan'] = get_object_or_404(BoxDonJuan, office=partner.office)
            self.__add_don_juan_movement(data)
            data_partner = {
                'user': partner.user,
                'office': target_office,
                'partner_type': partner.partner_type,
                'direct_partner': partner.direct_partner
            }
            self.create_partner(data_partner)
            
