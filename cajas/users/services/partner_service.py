
from ..models.partner import Partner


class PartnerManager(object):

    PROPERTIES = ['user', 'office', 'partner_type', 'direct_partner', 'is_daily_square']

    @staticmethod
    def __validate_data(self, data):
        for property in self.PROPERTIES:
            if property not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_partner(self, data):
        self.__validate_data(self, data)
        partner = Partner.objects.create(
            user=data['user'],
            office=data['office'],
            partner_type=data['partner_type'],
            direct_partner=data['direct_partner'],
            is_daily_square=data['is_daily_square'],
        )
        return partner


partner_manager = PartnerManager()
