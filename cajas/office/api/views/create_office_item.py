
from rest_framework.generics import CreateAPIView
from cajas.office.models.officeItems import OfficeItems
from cajas.office.api.serializer.office_item_create_serializer import OfficeItemCreateSerializer


class CreateOfficeItem(CreateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemCreateSerializer
