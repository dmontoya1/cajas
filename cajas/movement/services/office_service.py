
from concepts.models.concepts import Concept

from ..models.movement_office import MovementOffice


class MovementOfficeManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_movement(self, data):
        self.__validate_data(data)
        movement = MovementOffice.objects.create(
            box_office=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
        )
        return movement

    def __get_movement_by_pk(self, pk):
        return MovementOffice.objects.filter(pk=pk)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def __update_movement_type(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance += (int(data['movement'].value) * 2)
        else:
            box.balance -= (int(data['movement'].value) * 2)
        box.save()

    def __update_value(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance -= int(data['movement'].value)
            box.balance += int(data['value'])
        else:
            box.balance += int(data['movement'].value)
            box.balance -= int(data['value'])
        box.save()

    def update_office_movement(self, data):
        current_movement_office = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_office.first()
        current_concept = self.__get_current_concept(data['concept'])
        object_data = dict()
        object_data['box_office'] = current_movement.box_office
        object_data['concept'] = current_concept
        object_data['value'] = data['value']
        object_data['movement_type'] = data['movement_type']
        object_data['detail'] = data['detail']
        object_data['date'] = data['date']
        data['movement'] = current_movement
        data['box'] = current_movement.box_office

        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            self.__update_movement_type(data)
        if self.__is_movement_value_updated(current_movement, data['value']):
            self.__update_value(data)
        current_movement_office.update(**object_data)
