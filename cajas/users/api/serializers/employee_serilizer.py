
from rest_framework import serializers

from cajas.users.models.employee import Employee
from .user_serializer import UserSerializer
from .charge_serializer import ChargeSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    """
    """

    user = UserSerializer(many=False, read_only=True)
    charge = ChargeSerializer(many=False, read_only=True)

    class Meta:
        model = Employee
        fields = (
            'id', 'user', 'office', 'charge', 'salary_type', 'salary',
            'passport', 'cv', 'is_daily_square', 'observations'
        )
