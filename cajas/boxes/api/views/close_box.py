
from rest_framework import generics

from ...models.box_daily_square import BoxDailySquare
from ..serializers.box_daily_square_serializer import BoxDailySquareSerializer

from api.CsrfExempt import CsrfExemptSessionAuthentication


class CloseBox(generics.UpdateAPIView):
    queryset = BoxDailySquare.objects.all()
    serializer_class = BoxDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
