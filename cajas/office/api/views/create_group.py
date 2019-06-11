
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.employee import Employee
from cajas.users.models.group import Group
from cajas.users.models.group_employee import GroupEmployee


class CreateGroup(APIView):

    def post(self, request, format=None):
        employee = Employee.objects.get(pk=request.data["admin"])
        office = OfficeCountry.office.get(pk=request.data['office'])
        group = Group.objects.create(admin=employee, office=office)
        for sup in request.POST.getlist("supervisors[]"):
            supervisor = Employee.objects.get(pk=sup)
            GroupEmployee.objects.create(
                group=group,
                supervisor=supervisor
            )
        return Response(
            'Se ha creado el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
