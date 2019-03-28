
from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.users.models.user import User
from chains.models.chain import Chain
from concepts.models.concepts import Concept
from concepts.services.stop_service import StopManager
from general_config.models.country import Country
from loans.models.loan import Loan
from office.models.office import Office
from units.models.units import Unit
from webclient.views.get_ip import get_ip
from webclient.views.utils import get_object_or_none

from ....services.daily_square_service import MovementDailySquareManager

daily_square_manager = MovementDailySquareManager()


class CreateWithdrawMovement(APIView):
    """
    """

    def post(self, request, format=None):
        if request.user.related_daily_box:
            box_daily_square = request.user.related_daily_box.get()
        else:
            return Response(
                'No tienes permisos para realizar el retiro. Solo el cuadre diario puede hacer el retiro',
                status=status.HTTP_400_BAD_REQUEST
            )
        concept = Concept.objects.get(name='Retiro de Socio')
        value = request.POST['value']
        detail = request.POST['detail']

        ip = get_ip(request)

        data = {
            'box': box_daily_square,
            'concept': concept,
            'date': datetime.now(),
            'movement_type': 'OUT',
            'value': value,
            'detail': detail,
            'responsible': request.user,
            'ip': ip,
            'unit': None,
            'user': None,
            'country': None,
            'office': None,
            'loan': None,
            'chain': None,
        }
        movement = daily_square_manager.create_movement(data)
        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
