
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cajas.users.models.employee import Employee
from cajas.users.models.group import Group
from cajas.users.models.group_employee import GroupEmployee


class CreateGroup(APIView):

    def post(self, request, format=None):
        admin = Group.objects.get(pk=request.data["admin"])
        for sup in request.POST.getlist("supervisors[]"):
            supervisor = Employee.objects.get(pk=sup)
            group = GroupEmployee.objects.create(
                group=admin,
                supervisor=supervisor
            )
        return Response(
            'Se ha creado el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
