
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.movement.services.partner_service import MovementPartnerManager

from ....models.movement_withdraw import MovementWithdraw

movement_partner_manager = MovementPartnerManager()


class DeclineWithdrawMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementWithdraw, pk=request.data['movement_id'])
        movement.delete()

        return Response(
            'El movimiento se ha rechazo exitosamente. No se ha creado el movimiento en la caja',
            status=status.HTTP_201_CREATED
        )
