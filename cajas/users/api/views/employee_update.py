from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer
from movement.api.views.CsrfExempt import CsrfExemptSessionAuthentication

User = get_user_model()


class EmployeeUpdate(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        item = Employee.objects.get(pk=kwargs['pk'])
        user = User.objects.get(pk=item.user.pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        item.user = user
        item.salary = request.data["salary"]
        # item.charge = request.data["charge"]
        item.save()
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_201_CREATED
        )
