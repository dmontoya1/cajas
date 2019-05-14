
from rest_framework import generics

from ...models.user_place_pay import UserPlacePay
from ..serializers.user_place_pay_serializer import UserPlacePaySerializer


class UserPlacePayCreate(generics.CreateAPIView):
    """
    """

    serializer_class = UserPlacePaySerializer
    queryset = UserPlacePay.objects.all()
