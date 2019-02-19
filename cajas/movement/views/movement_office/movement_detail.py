
from rest_framework import generics

from ...models.movement_office import MovementOffice
from ...serializers.movement_office_serializer import MovementOfficeSerializer


class MovementOfficeDetail(generics.RetrieveAPIView):
    """
    """

    serializer_class = MovementOfficeSerializer
    queryset = MovementOffice.objects.all()
