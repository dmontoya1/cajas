from rest_framework.generics import ListAPIView

from cajas.users.models.partner import Partner
from cajas.users.api.serializers.partner_serializer import PartnerSerializer


class PartnerList(ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_queryset(self, *args, **kwargs):
        return Partner.objects.filter(pk=self.kwargs['pk'])
