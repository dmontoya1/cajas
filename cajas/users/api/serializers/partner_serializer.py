from rest_framework import serializers
from cajas.users.models.partner import Partner
from .user_serializer import UserSerializer


class PartnerSerializer(serializers.ModelSerializer):
    """
    """

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Partner
        fields = ('pk', 'user')
