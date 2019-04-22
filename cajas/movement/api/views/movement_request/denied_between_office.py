from rest_framework.views import APIView
from rest_framework import status

from api.CsrfExempt import CsrfExemptSessionAuthentication

from ....models.movement_between_office_request import MovementBetweenOfficeRequest
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class DeclineBetweenOfficeMovement(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        movement = get_object_or_404(
            MovementBetweenOfficeRequest,
            pk=request.data['movement_id']
        )
        movement.delete()
        return Response(
            'El movimiento se ha rechazo exitosamente. No se ha creado el movimiento en la caja',
            status=status.HTTP_201_CREATED
        )
