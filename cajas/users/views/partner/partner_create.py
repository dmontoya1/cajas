
from ...models.partner import Partner


class PartnerCreate(object):
    """
    """

    def __init__(self, data):
        self._user = data['user']
        self._office = data['office']
        self._partner_type = data['partner_type']
        self._direct_partner = data['direct_partner']
        self._is_daily_square = data['is_daily_square']

    def call(self):
        partner = Partner(
            user=self._user,
            office=self._office,
            partner_type=self._partner_type,
            direct_partner=self._direct_partner,
            is_daily_square=self._is_daily_square,
        )
        partner.save()
        return partner
