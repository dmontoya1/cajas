

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication

from ...services.employee_service import EmployeeManager


class DailySquareUnitsUpdate(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        employee_manager = EmployeeManager()
        employee_manager.update_daily_square_units_group(request.data)
        return Response(
            'El empleado se ha creado correctamente',
            status=status.HTTP_201_CREATED
        )
