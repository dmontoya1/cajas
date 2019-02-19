
from .create_movement_service_simple import CreateMovementSimpleService
from .create_movement_service_double import CreateMovementDoubleService
from .create_movement_service_simple_double import CreateMovementSimpleDoubleService
from .create_new_partner_movements import CreateNewPartnerMovements


class MovementPartnerHandler(object):

    @classmethod
    def create_simple(cls, data):
        return CreateMovementSimpleService(data).call()

    @classmethod
    def create_double(cls, data):
        return CreateMovementDoubleService(data).call()

    @classmethod
    def create_simple_double(cls, data):
        return CreateNewPartnerMovements(data).call()

    @classmethod
    def create_partner_movements(cls, data):
        """función para crear los movimientos cuando se crea un nuevo socio, y éste entra
        con precio inicial > 0
        """
        return CreateNewPartnerMovements(data).call()
