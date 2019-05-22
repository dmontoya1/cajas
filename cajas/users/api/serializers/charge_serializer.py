from rest_framework import serializers

from cajas.users.models.charges import Charge


class ChargeSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Charge
        fields = '__all__'
