from rest_framework.generics import ListAPIView

from office.models.officeItems import OfficeItems
from office.serializer.office_item_serializer import OfficeItemSerializer


class OfficeItemList(ListAPIView):
    serializer_class = OfficeItemSerializer

    def get_queryset(self, *args, **kwargs):
        return OfficeItems.objects.filter(pk=self.kwargs['pk'])
