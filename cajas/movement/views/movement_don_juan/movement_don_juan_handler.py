
from .create_movement_service import CreateMovementService


class MovementDonJuanHandler(object):

    @staticmethod
    def create(data):
        return CreateMovementService(data).call()
