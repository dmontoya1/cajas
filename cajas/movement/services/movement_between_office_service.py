

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
        converted_value = self.movement_currency_value_convertion(
            data['value'], data['office'],
            data['destine_office']
        )
        self.create_between_offices_movement_request_instance(
            data, concept, contrapart,
            converted_value, data['destine_office']
        )

    def movement_currency_value_convertion(
        self, origin_value,
        origin_office, destine_office
    ):
        if origin_office.country == destine_office.country:
            return origin_value
        ex_destine = Exchange.objects.get(currency=destine_office.country.currency)
        if destine_office.country.abbr == "COL":
            return float(ex_destine.exchange_cop)*float(origin_value)
        elif origin_office.country.abbr != "COL":
            ex_origin = Exchange.objects.get(currency=origin_office.country.currency)
            origin_to_cop = float(ex_origin.exchange_cop)*float(origin_value)
            return float(origin_to_cop)/float(ex_destine.exchange_cop)
        else:
            return float(origin_value)/float(ex_destine.exchange_cop)

    def create_between_offices_movement_request_instance(
        self, data, concept, contrapart,
        converted_value, destine_office
    ):
        mv = MovementBetweenOfficeRequest.objects.create(
            box_office=destine_office.box,
            observation=data['detail'],
            detail=data['detail'],
            concept=concept,
            movement_type=contrapart,
            date=data['date'],
            value=converted_value,
            responsible=data['responsible'],
            ip=data['ip'],
        )
