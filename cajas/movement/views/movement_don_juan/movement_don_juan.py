
from .create_movement_service import CreateMovementService


class MovementDonJuan(object):

    @classmethod
    def create(cls, data):
        return CreateMovementService(data).call()
