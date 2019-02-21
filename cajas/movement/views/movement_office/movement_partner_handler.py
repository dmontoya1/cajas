
from .create_movement import CreateMovementOffice


class MovementPartnerHandler(object):

    @staticmethod
    def create_movement(data):
        return CreateMovementOffice(data).call()
