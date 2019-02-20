
from .create_movement_service_simple import CreateMovementSimpleService
from .create_movement_service_double import CreateMovementDoubleService
from .create_movement_service_simple_double import CreateMovementSimpleDoubleService
from .create_new_partner_movements import CreateNewPartnerMovements


class MovementPartnerHandler(object):

    @staticmethod
    def create_simple(data):
        return CreateMovementSimpleService(data).call()

    @staticmethod
    def create_double(data):
        return CreateMovementDoubleService(data).call()

    @staticmethod
    def create_simple_double(data):
        return CreateNewPartnerMovements(data).call()

    @staticmethod
    def create_partner_movements(data):
        """función para crear los movimientos cuando se crea un nuevo socio, y éste entra
        con precio inicial > 0
        """
        return CreateNewPartnerMovements(data).call()
