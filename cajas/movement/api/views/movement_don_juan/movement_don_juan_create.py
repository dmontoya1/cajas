
from rest_framework import generics

from ....models.movement_don_juan import MovementDonJuan
from ...serializers.movement_don_juan_serializer import MovementDonJuanSerializer


class MovementDonJuanCreate(generics.CreateAPIView):
    """
    """

    serializer_class = MovementDonJuanSerializer
    queryset = MovementDonJuan.objects.all()
