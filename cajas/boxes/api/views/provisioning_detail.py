from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from api.CsrfExempt import CsrfExemptSessionAuthentication


class ProvisioningDetail(generics.RetrieveUpdateAPIView):
    queryset = OfficeItems.objects.all()
    serializer_class = OfficeItemSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):

        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
