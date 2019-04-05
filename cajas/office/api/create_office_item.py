
from rest_framework.generics import CreateAPIView
from office.models.officeItems import OfficeItems
from office.serializer.office_item_create_serializer import OfficeItemCreateSerializer


class CreateOfficeItem(CreateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemCreateSerializer
