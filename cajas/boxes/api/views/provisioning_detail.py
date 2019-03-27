from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from movement.models.movement_provisioning import MovementProvisioning
from boxes.api.serializers.provisioning_serializer import ProvisioningSerializer

from api.CsrfExempt import CsrfExemptSessionAuthentication


class ProvisioningDetail(generics.RetrieveUpdateAPIView):
    queryset = MovementProvisioning.objects.all()
    serializer_class = ProvisioningSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        print(request.data)
        item = MovementProvisioning.objects.get(pk=kwargs['pk'])
        item.date = request.data["date"]
        item.movement_type = request.data["movement_type"]
        item.value = request.data["value"]
        item.detail = request.data["detail"]
        item.save()
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
