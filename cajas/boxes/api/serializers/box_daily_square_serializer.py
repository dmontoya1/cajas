
from rest_framework import serializers

from ...models.box_daily_square import BoxDailySquare


class BoxDailySquareSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxDailySquare
        fields = (
            'id', 'user', 'office', 'balance',
            'is_active', 'last_movement_id', 'is_closed'
        )
