from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from ...models.units import Unit
from cajas.units.api.serializers.unit_serializer import UnitSerializer


class UnitDelete(generics.DestroyAPIView):
    serializer_class = UnitSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def destroy(self, request, *args, **kwargs):
        unit = Unit.objects.get(pk=kwargs['pk'])
        unit.description = request.data['description']
        unit.is_active = False
        unit.save()
        return Response(
            'La unidad se ha eliminado correctamente',
            status=status.HTTP_200_OK
        )
