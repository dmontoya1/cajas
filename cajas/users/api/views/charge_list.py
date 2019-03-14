from rest_framework.generics import ListAPIView

from models.charges import Charge
from cajas.users.api.serializers.charge_serializer import ChargeSerializer


class ChargeList(ListAPIView):
    serializer_class = Charge

