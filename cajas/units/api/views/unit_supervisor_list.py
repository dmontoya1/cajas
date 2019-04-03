
from rest_framework import generics

from ...models.units import Unit
from ..serializers.unit_serializer import UnitSerializer


class UnitSupervisorList(generics.ListAPIView):
    """
    """

    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.filter(supervisor__pk=self.kwargs['pk'])
