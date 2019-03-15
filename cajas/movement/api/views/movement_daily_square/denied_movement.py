
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from concepts.models.concepts import Relationship
from api.CsrfExempt import CsrfExemptSessionAuthentication
from movement.views.movement_partner.create_movement_service_simple import CreateMovementSimpleService
from movement.views.movement_country.create_movement import CreateMovementCountry
from movement.views.movement_office.create_movement import CreateMovementOffice
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare


class DeniedMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        movement.denied_detail = request.data['text']
        movement.review = True
        movement.status = MovementDailySquare.DENIED
        movement.save()

        return Response(
            'El movimiento se ha rechazado exitosamente. No se creó ningún movimiento en otra caja',
            status=status.HTTP_201_CREATED
        )
