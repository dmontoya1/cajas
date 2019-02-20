
from .create_movement_service import CreateMovementService


class MovementDonJuan(object):

    @staticmethod
    def create(cls, data):
        return CreateMovementService(data).call()
