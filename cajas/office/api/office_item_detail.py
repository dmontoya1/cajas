from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from movement.api.views.CsrfExempt import CsrfExemptSessionAuthentication

from inventory.models.brand import Brand
from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer


class OfficeItemDetail(generics.RetrieveUpdateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        item = OfficeItems.objects.get(pk=kwargs['pk'])
        item.name = request.data["name"]
        item.category = request.data["category"]
        item.price = request.data["price"]
        item.description = request.data["description"]
        item.brand = Brand.objects.filter(pk=request.data["brand"])[0]
        item.save()
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_201_CREATED
        )
