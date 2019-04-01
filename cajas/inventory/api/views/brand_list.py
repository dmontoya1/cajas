from rest_framework.generics import ListAPIView

from ...models.brand import Brand
from ..serializer.brand_serializer import BrandSerializer
from inventory.models.brand import Brand
from inventory.api.serializer.brand_serializer import BrandSerializer


class BrandList(ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self, *args, **kwargs):
        return Brand.objects.filter(category__pk=self.kwargs['pk'])
