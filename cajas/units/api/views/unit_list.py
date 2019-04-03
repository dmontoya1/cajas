
from rest_framework import generics

from ...models.units import Unit
from ..serializers.unit_serializer import UnitSerializer


class UnitList(generics.ListAPIView):
    """
    """

    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.filter(partner__pk=self.kwargs['pk'])
