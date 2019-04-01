
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication
from core.services.email_service import EmailManager
from movement.services.daily_square_service import MovementDailySquareManager

from ....models.movement_withdraw import MovementWithdraw

email_manager = EmailManager()
movement_daily_manager = MovementDailySquareManager()


class AcceptWithDrawRequestMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementWithdraw, pk=request.data['movement_id'])
        data = {
            'concept': movement.concept,
            'date': movement.date,
            'movement_type': movement.movement_type,
            'value': movement.value,
            'detail': movement.detail,
            'responsible': movement.responsible,
            'ip': movement.ip,
            'unit': None,
            'user': movement.box_partner.partner.user,
            'country': None,
            'office': None,
            'loan': None,
            'chain': None,
        }
        if movement.box_daily_square:
            data['box'] = movement.box_daily_square
            movement_daily_manager.create_movement(data)
            email_manager.send_withdraw_accept_email(request, movement.box_daily_square.user.email)
        else:
            data['box'] = movement.box_partner
        movement.delete()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
