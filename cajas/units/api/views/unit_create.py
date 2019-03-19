from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from units.models.units import Unit
from units.api.serializers.unit_serializer import UnitSerializer
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication

User = get_user_model()
user_manager = UserManager()


class EmployeeCreate(generics.CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
