from rest_framework.generics import ListAPIView

from cajas.users.models.charges import Charge
from cajas.users.api.serializers.charge_serializer import ChargeSerializer


class ChargeList(ListAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
