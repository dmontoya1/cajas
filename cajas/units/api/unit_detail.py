
from rest_framework import generics

from ..models.units import Unit
from ..serializers.unit_serializer import UnitSerializer


class UnitDetail(generics.RetrieveAPIView):
    """
    """

    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
