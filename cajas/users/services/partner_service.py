
from ..models.partner import Partner


class PartnerManager(object):

    PROPERTIES = ['user', 'office', 'partner_type', 'direct_partner', ]

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_partner(self, data):
        self.__validate_data(data)
        partner = Partner.objects.create(
            user=data['user'],
            office=data['office'],
            partner_type=data['partner_type'],
            direct_partner=data['direct_partner'],
        )
        return partner


partner_manager = PartnerManager()
