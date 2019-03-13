
from rest_framework.generics import CreateAPIView
from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer


class CreateOfficeItem(CreateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemSerializer
