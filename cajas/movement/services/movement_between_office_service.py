

from cajas.concepts.models.concepts import Concept
from cajas.general_config.models.exchange import Exchange
from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest
from cajas.office.models.notifications import Notifications
from cajas.office.models.officeCountry import OfficeCountry


class MovementBetweenOfficesManager(object):

    def create_between_offices_movement_request(self, data):
        concept = data['concept']
        if data['movement_type'] == 'OUT':
            contrapart = 'IN'
        else:
            contrapart = 'OUT'

        self.create_between_offices_movement_request_instance(
            data, concept, contrapart,
            data['value'], data['destine_office'],
            data['office']
        )

    def create_between_offices_movement_request_instance(
        self, data, concept, contrapart,
        converted_value, destine_office, origin_office
    ):
        mv = MovementBetweenOfficeRequest.objects.create(
            box_office=destine_office.box,
            origin_office=office.box,
            observation=data['detail'],
            detail=data['detail'],
            concept=concept,
            movement_type=contrapart,
            date=data['date'],
            value=converted_value,
            responsible=data['responsible'],
            ip=data['ip'],
        )
