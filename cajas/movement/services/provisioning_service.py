
from ..models.movement_provisioning import MovementProvisioning


class MovemenProvisioningManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_movement(self, data):
        self.__validate_data(data)
        movement = MovementProvisioning.objects.create(
            box_provisioning=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
        )
        return movement
