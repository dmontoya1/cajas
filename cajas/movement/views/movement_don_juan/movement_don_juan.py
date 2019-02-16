
from .create_movement_service import CreateMovementService


class MovementDonJuan(object):

    @classmethod
    def create(cls, box, concept, movement_type, value, detail, date, responsible, ip):
        return CreateMovementService(
            box,
            concept,
            movement_type,
            value,
            detail,
            date,
            responsible,
            ip
        ).call()
