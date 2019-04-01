
from office.models.officeItems import OfficeItems


class OfficeItemsManager(object):

    PROPERTIES = ['office', 'name', 'description', 'price', 'brand']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_office_item(self, data):
        self.__validate_data(data)
        office_item = OfficeItems.objects.create(
            office=data['office'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            brand=data['brand'],
        )
        return office_item
