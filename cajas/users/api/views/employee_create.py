from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.users.services.user_service import UserManager
from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer

User = get_user_model()


class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def post(self, request, *args, **kwargs):
        request.data["username"] = request.data["email"]
        user_service = UserManager()
        user = user_service.create_user(request.data)

        print(request.data) 
        print(request.FILES)

        if request.data["password1"] == '':
            user.is_abstract = False
            user.is_active = False
        else:
            user.is_active = True
            user.is_abstract = True
            password = make_password(request.data['password'])
            user.password = password
        # user.save()
        employee = Employee()
        employee.salary = request.data["salary"]
        employee.salary_type = request.data["salary_type"]
        employee.user = user
        # employee.save()
        return Response(
            'El empleado se ha creado correctamente',
            status=status.HTTP_201_CREATED
        )