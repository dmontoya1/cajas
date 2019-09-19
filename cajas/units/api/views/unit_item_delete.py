
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from ...models.unitItems import UnitItems
from cajas.units.api.serializers.unit_items_serializer import UnitItemSerializer


class UnitItemDelete(generics.DestroyAPIView):
    serializer_class = UnitItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def destroy(self, request, *args, **kwargs):
        item = UnitItems.objects.get(pk=kwargs['pk'])
        item.observations = request.data['description']
        item.is_deleted = True
        item.save()
        return Response(
            'La unidad se ha eliminado correctamente',
            status=status.HTTP_200_OK
        )
