
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer

User = get_user_model()


class EmployeeUpdate(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        charge = Charge.objects.get(pk=request.data["charge"])
        item = Employee.objects.get(pk=kwargs['pk'])
        user = User.objects.get(pk=item.user.pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        if request.data['is_daily_square'] == "true":
            user.is_daily_square = True
        if "password1" in request.data:
            user.password = make_password(request.data['password1'])
            user.is_abstract = True
        else:
            user.is_abstract = False
        user.save()
        item.user = user
        item.salary = request.data["salary"]
        item.charge = charge
        if request.data["cv"] != 'undefined':
            item.cv = request.data["cv"]
        if request.data["passport"] != 'undefined':
            item.passport = request.data["passport"]
        item.save()
        return Response(
            'El empleado se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
