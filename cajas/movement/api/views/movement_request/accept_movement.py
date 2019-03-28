
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication
from movement.services.partner_service import MovementPartnerManager

from ....models.movement_request import MovementRequest

movement_partner_manager = MovementPartnerManager()


class AcceptRequestMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementRequest, pk=request.data['movement_id'])
        data = {
            'box': movement.box_partner,
            'concept': movement.concept,
            'date': movement.date,
            'movement_type': movement.movement_type,
            'value': movement.value,
            'detail': movement.detail,
            'responsible': movement.responsible,
            'ip': movement.ip,
        }
        movement_partner_manager.create_simple(data)
        movement.delete()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
