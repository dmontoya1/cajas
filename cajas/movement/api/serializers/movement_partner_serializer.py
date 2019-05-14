
from rest_framework import serializers

from ...models.movement_partner import MovementPartner


class MovementPartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementPartner
        fields = ('__all__')

