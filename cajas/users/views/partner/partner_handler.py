
from .partner_create import PartnerCreate


class PartnerHandler(object):
    """
    """

    @staticmethod
    def partner_create(data):
        return PartnerCreate(data).call()
