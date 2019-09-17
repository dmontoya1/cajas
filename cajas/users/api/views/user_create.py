
from django.db import IntegrityError
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cajas.boxes.services.box_daily_square_manager import BoxDailySquareManager
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.services.user_service import UserManager
from cajas.users.services.partner_service import PartnerManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.movement.services.daily_square_service import MovementDailySquareManager
from cajas.office.models.officeCountry import OfficeCountry

user_manager = UserManager()


class UserCreate(APIView):
    """
    """

    def post(self, request, format=None):
        user_manager.create_user(request.data)
        return Response(
            'Se ha creado el usuario exitosamente.',
            status=status.HTTP_201_CREATED
        )
