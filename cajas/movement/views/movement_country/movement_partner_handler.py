
from .create_movement import CreateMovementCountry


class MovementPartnerHandler(object):

    @staticmethod
    def create_movement(data):
        return CreateMovementCountry(data).call()
