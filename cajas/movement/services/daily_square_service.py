
from ..models.movement_daily_square import MovementDailySquare


class MovementDailySquareManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip',
                  'unit', 'user', 'country', 'office', 'loan', 'chain']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_movement(self, data):
        self.__validate_data(data)
        movement = MovementDailySquare.objects.create(
            box_daily_square=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
            unit=data['unit'],
            user=data['user'],
            country=data['country'],
            office=data['office'],
        )
        return movement
