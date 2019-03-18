from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status

from api.CsrfExempt import CsrfExemptSessionAuthentication
from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer


class OfficeItemDelete(generics.DestroyAPIView):
    serializer_class = OfficeItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def destroy(self, request, *args, **kwargs):
        item = OfficeItems.objects.get(pk=kwargs['pk'])
        item.description = request.data['description']
        item.is_deleted = True
        item.save()
        return Response(
            'El item se ha eliminado correctamente',
            status=status.HTTP_200_OK
        )
