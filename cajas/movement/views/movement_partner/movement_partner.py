
from .create_movement_service_simple import CreateMovementSimpleService
from .create_movement_service_double import CreateMovementDoubleService
from .create_movement_service_simple_double import CreateMovementSimpleDoubleService
from .create_new_partner_movements import CreateNewPartnerMovements


class MovementPartner(object):

    @classmethod
    def create_simple(cls, box, concept, movement_type, value, detail, date, reponsible, ip):
        return CreateMovementSimpleService(
            box,
            concept,
            movement_type,
            value,
            detail,
            date,
            value,
            reponsible,
            ip
        ).call()

    @classmethod
    def create_double(cls, partner, concept, movement_type, value, detail, date, reponsible, ip):
        return CreateMovementDoubleService(
            partner,
            concept,
            movement_type,
            value,
            detail,
            date,
            value,
            reponsible,
            ip
        ).call()

    @classmethod
    def create_simple_double(cls, partner, concept, movement_type, value, detail, date, reponsible, ip):
        return CreateNewPartnerMovements(
            partner,
            concept,
            movement_type,
            value,
            detail,
            date,
            reponsible,
            ip
        ).call()

    @classmethod
    def create_partner_movements(cls, partner, value, reponsible, ip):
        """función para crear los movimientos cuando se crea un nuevo socio, y éste entra
        con precio inicial > 0
        """
        return CreateNewPartnerMovements(partner, value, reponsible, ip).call()
