
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


from cajas.users.models.group_employee import GroupEmployee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer
from .group_serializer import GroupSerializer


class GroupEmployeeSerializer(serializers.ModelSerializer):

    supervisor = EmployeeSerializer(many=False, read_only=True)
    group = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = GroupEmployee
        fields = ('group', 'supervisor')
