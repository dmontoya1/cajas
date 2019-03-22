from rest_framework import serializers
from cajas.users.models.partner import Partner
from .user_serializer import UserSerializer


class PartnerSerializer(serializers.ModelSerializer):
    """
    """

    user = UserSerializer(many=False, read_only=True)
    partner_type = serializers.SerializerMethodField()
    direct_partner = serializers.StringRelatedField(many=True)

    class Meta:
        model = Partner
        fields = ('pk', 'code', 'partner_type', 'direct_partner', 'user')

    def get_partner_type(self, obj):
        return str(obj.partner_type)
