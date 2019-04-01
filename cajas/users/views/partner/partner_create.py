
from ...models.partner import Partner


class PartnerCreate(object):
    """
    """

    def __init__(self, data):
        try:
            self._user = data['user']
            self._office = data['office']
            self._partner_type = data['partner_type']
            self._direct_partner = data['direct_partner']
        except:
            raise ValidationError('Todos los datos son obligatorios')

    def call(self):
        partner = Partner.objects.create(
            user=self._user,
            office=self._office,
            partner_type=self._partner_type,
            direct_partner=self._direct_partner,
        )
        return partner
