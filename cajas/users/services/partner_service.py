


class PartnerManager():

    PROPERTIES = ['user', 'office']


    @staticmethod
    def __validate_data(self, data):
        for property in self.PROPERTIES:
            if property not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_partner(self, data):
        self.__validate_data(data)
        partner = Partner.objects.create(
            user=self._user,
            office=self._office,
            partner_type=self._partner_type,
            direct_partner=self._direct_partner,
            is_daily_square=self._is_daily_square,
        )
        return partner

    def delete_parter(self):
        pass

    def get_partner_by_id(self, id):



partner_manager = PartnerManager()
partner_manager.create_partner(data)
partner_object = partner_manager.get_partner_by_id(id)
