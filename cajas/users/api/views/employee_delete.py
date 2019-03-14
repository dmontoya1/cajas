from django.contrib.auth import get_user_model

from rest_framework import generics 
from rest_framework.response import Response
from rest_framework import status

from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer
from movement.api.views.CsrfExempt import CsrfExemptSessionAuthentication

User = get_user_model()


class EmployeeDelete(generics.DestroyAPIView):
    serializer_class = EmployeeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def destroy(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=kwargs['pk'])
        employee.observations = request.data['description']
        user = User.objects.get(pk=employee.user.pk)
        user.is_active = False
        user.is_abstract = False
        user.save()
        employee.user = user
        employee.save()

        return Response(
            'El item se ha eliminado correctamente',
            status=status.HTTP_201_CREATED
        )
