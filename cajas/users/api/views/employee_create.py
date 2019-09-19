import copy

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.boxes.services.box_daily_square_manager import BoxDailySquareManager
from cajas.users.services.user_service import UserManager
from cajas.users.services.employee_service import EmployeeManager
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.charges import Charge

box_daily_square_manager = BoxDailySquareManager()
employee_manager = EmployeeManager()
User = get_user_model()
user_manager = UserManager()


class EmployeeCreate(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        aux = dict()
        user = user_manager.create_user(request.data)
        office = OfficeCountry.objects.get(pk=request.data["office"])
        charge = Charge.objects.get(pk=request.data["charge"])

        aux['user'] = user
        aux['charge'] = charge
        aux['office'] = office

        employee_manager.create_employee(request.data, aux)
        for g in request.data.getlist("groups[]"):
            group = Group.objects.get(pk=g)
            group.user_set.add(user)
        if request.data["is_daily_square"] == "true":
            box_daily_square_manager.create_box(aux)

        return Response(
            'El empleado se ha creado correctamente',
            status=status.HTTP_201_CREATED
        )
