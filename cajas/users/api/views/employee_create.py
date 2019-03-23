import copy

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from cajas.users.services.user_service import UserManager
from cajas.users.services.employee_service import EmployeeManager
from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from office.models.office import Office
from cajas.users.models.charges import Charge

User = get_user_model()
user_manager = UserManager()
employee_manager = EmployeeManager()


class EmployeeCreate(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        print(request.data)
        print(request.FILES)
        aux = copy.deepcopy(request.data)
        user = user_manager.create_user(request.data)
        office = Office.objects.get(pk=request.data["office"])
        charge = Charge.objects.get(pk=request.data["charge"])

        aux['user'] = user
        aux['charge'] = charge
        aux['office'] = office

        employee = employee_manager.create_employee(aux)

        return Response(
            'El empleado se ha creado correctamente',
            status=status.HTTP_201_CREATED
        )
