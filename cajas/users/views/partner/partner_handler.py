
from .partner_create import PartnerCreate


class PartnerHandler(object):
    """
    """

    @classmethod
    def partner_create(cls, data):
        return PartnerCreate(data).call()
