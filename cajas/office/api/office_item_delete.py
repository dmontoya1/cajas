from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status

from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer
from movement.api.views.CsrfExempt import CsrfExemptSessionAuthentication


class OfficeItemDelete(generics.DestroyAPIView):
    serializer_class = OfficeItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def destroy(self, request, *args, **kwargs):
        desc = request.data['description']
        item = OfficeItems.objects.get(pk=kwargs['pk'])
        item.description = desc
        item.is_deleted = True
        item.save()
        return Response(
            'El item se ha eliminado correctamente',
            status=status.HTTP_201_CREATED
        )
