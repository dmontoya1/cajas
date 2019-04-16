
from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.users.models.partner import Partner
from concepts.models.concepts import Concept
from webclient.views.get_ip import get_ip

from ....services.daily_square_service import MovementDailySquareManager
from ....services.partner_service import MovementPartnerManager

daily_square_manager = MovementDailySquareManager()
movement_partner_manager = MovementPartnerManager()


class CreateWithdrawMovement(APIView):
    """
    """

    def post(self, request, format=None):
        concept = Concept.objects.get(name='Retiro de Socio')
        partner = get_object_or_404(Partner, pk=request.POST['partner'])
        data = {
            'concept': concept,
            'date': datetime.now(),
            'movement_type': 'OUT',
            'value': request.POST['value'],
            'detail': 'Retiro Socio {}'.format(partner),
            'responsible': request.user,
            'ip': get_ip(request),
            'unit': None,
            'user': partner.user,
            'country': None,
            'office': None,
            'loan': None,
            'chain': None,
        }
        if request.user.related_daily_box and request.user.is_daily_square:
            box_daily_square = request.user.related_daily_box.get()
            data['box'] = box_daily_square
            movement = daily_square_manager.create_movement(data)
        else:
            data['box'] = partner.box
            data['partner'] = partner
            movement = movement_partner_manager.create_withdraw_movement_full(data)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
