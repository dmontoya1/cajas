
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication

from ....models.movement_daily_square import MovementDailySquare
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem

from units.models.unitItems import UnitItems
from units.models.units import Unit

class DeniedMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        if movement.concept.name == "Compra de Inventario Unidad" and movement.concept.name == "Compra ":
            MovementDailySquareRequestItem.objects.filter(movement=movement).delete()
        box = movement.box_daily_square
        movement.denied_detail = request.data['text']
        movement.review = True
        movement.status = MovementDailySquare.DENIED
        movement.save()
        if movement.movement_type == 'IN':
            box.balance -= movement.value
        else:
            box.balance += movement.value
        box.save()
        return Response(
            'El movimiento se ha rechazado exitosamente. No se creó ningún movimiento en otra caja',
            status=status.HTTP_201_CREATED
        )
