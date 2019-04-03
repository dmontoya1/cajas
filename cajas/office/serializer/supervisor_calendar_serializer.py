
from rest_framework.response import Response
from rest_framework import serializers


from ..models.supervisorCalendar import SupervisorCalendar


class SupervisorCalendarSerializer(serializers.ModelSerializer):

    office = serializers.StringRelatedField(many=False, read_only=True)
    supervisor = serializers.StringRelatedField(many=False, read_only=True)
    unit = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = SupervisorCalendar
        fields = ('office', 'supervisor', 'unit', 'assigned_date')
