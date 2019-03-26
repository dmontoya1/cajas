
from rest_framework import serializers

from ...models.user_place_pay import UserPlacePay


class UserPlacePaySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = UserPlacePay
        fields = ('id', 'user_place', 'pay_value', 'date')
