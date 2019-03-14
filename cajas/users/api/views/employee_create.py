from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer

User = get_user_model()


class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        user = User()
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        '''= request.data["document_type"]
        = request.data["document_id"]
        = request.data["email"]
        = request.data["salary_type"]
        '''        
        employee = Employee()
        employee.salary = request.data["salary"]
        employee.salary_type = request.data["salary_type"]
        employee.user = user
        return Response(
            'El item se ha eliminado correctamente',
            status=status.HTTP_201_CREATED
        )
