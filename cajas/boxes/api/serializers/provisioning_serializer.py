
from rest_framework import serializers

from movement.models.movement_provisioning import MovementProvisioning


class ProvisioningSerializer(serializers.ModelSerializer):

    concept = serializers.StringRelatedField(many=False)

    class Meta:
        model = MovementProvisioning
        fields = (
            'id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_provisioning'
        )
