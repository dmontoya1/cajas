
from rest_framework import serializers

from boxes.models.box_provisioning import BoxProvisioning


class ProvisioningSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoxProvisioning
        fields = (
            'id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_office'
        )
