import copy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from boxes.models.box_provisioning import BoxProvisioning
from movement.models.movement_provisioning import MovementProvisioning
from boxes.api.serializers.provisioning_serializer import ProvisioningSerializer

from movement.services.provisioning_service import MovemenProvisioningManager
from webclient.views.get_ip import get_ip
from concepts.models.concepts import Concept

movement_provisioning_manager = MovemenProvisioningManager()


class ProvisioningCreate(APIView):

    def post(self, request, format=None):
        print(request.data)
        aux = copy.deepcopy(request.data)

        aux["box"] = get_object_or_404(BoxProvisioning, office__pk=request.data["office"])
        aux["responsible"] = request.user
        aux["ip"] = get_ip(request)
        aux["concept"] = get_object_or_404(Concept, pk=request.data["concept"])

        movement_provisioning_manager.create_movement(aux)

        return Response(
            'Se ha creado el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
