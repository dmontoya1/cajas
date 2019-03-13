from rest_framework import generics

from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer


class OfficeItemDetail(generics.RetrieveUpdateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemSerializer
