
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from units.models.units import Unit
from units.api.serializers.unit_create_serializer import UnitCreateSerializer


class UnitCreate(generics.CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitCreateSerializer
