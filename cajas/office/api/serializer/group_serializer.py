
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status


from cajas.users.models.group import Group
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer


class GroupSerializer(serializers.ModelSerializer):

    admin = EmployeeSerializer(many=False, read_only=True)

    class Meta:
        model = Group
        fields = ('pk', 'admin',)
