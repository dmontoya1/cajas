
from .create_movement_service_simple import CreateMovementSimpleService
from .create_movement_service_double import CreateMovementDoubleService
from .create_movement_service_simple_double import CreateMovementSimpleDoubleService
from .create_new_partner_movements import CreateNewPartnerMovements


class MovementPartner(object):

    @classmethod
    def create_simple(cls, box, concept, movement_type, value, detail, date, responsible, ip):
        return CreateMovementSimpleService(
            box,
            concept,
            movement_type,
            value,
            detail,
            date,
            responsible,
            ip
        ).call()

    @classmethod
    def create_double(cls, partner, concept, movement_type, value, detail, date, responsible, ip):
        return CreateMovementDoubleService(
            partner=partner,
            concept=concept,
            movement_type=movement_type,
            value=value,
            detail=detail,
            date=date,
            responsible=responsible,
            ip=ip
        ).call()

    @classmethod
    def create_simple_double(cls, partner, concept, movement_type, value, detail, date, responsible, ip):
        return CreateNewPartnerMovements(
            partner=partner,
            concept=concept,
            movement_type=movement_type,
            value=value,
            detail=detail,
            date=date,
            responsible=responsible,
            ip=ip
        ).call()

    @classmethod
    def create_partner_movements(cls, partner, value, responsible, ip):
        """función para crear los movimientos cuando se crea un nuevo socio, y éste entra
        con precio inicial > 0
        """
        return CreateNewPartnerMovements(partner, value, responsible, ip).call()
