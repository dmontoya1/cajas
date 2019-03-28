from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.users.models.employee import Employee

from api.CsrfExempt import CsrfExemptSessionAuthentication
from ...models.units import Unit
from ..serializers.unit_serializer import UnitSerializer

User = get_user_model()


class UnitDetail(generics.RetrieveUpdateAPIView):
    """
    """

    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        unit = Unit.objects.get(pk=kwargs['pk'])
        unit.name = request.data["name"]
        collector = User.objects.get(pk=request.data['collector'])
        supervisor = User.objects.get(pk=request.data['supervisor'])
        unit.collector = collector
        unit.supervisor = supervisor
        unit.save()
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
