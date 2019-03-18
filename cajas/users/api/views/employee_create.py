from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from cajas.users.services.user_service import UserManager
from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication

User = get_user_model()
user_manager = UserManager()


class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):

        # print(request.data['data']) #.append('username', request.data['data'].get('email')) 
        print(request.data)
        print(request.FILES)


        #user = user_manager.create_user(request.data)
        # request.data['user'] = 'user :D'
        # print(request.data)

        '''serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid:
            serializer.save()'''

        #print(request.data['cv'])
        #print(request.data['passport'])

        # employee = Employee()
        # employee.salary = request.data["salary"]
        # employee.salary_type = request.data["salary_type"]
        # employee.user = user
        # employee.save()

        return Response(
            'El empleado se ha creado correctamente',
            status=status.HTTP_201_CREATED
        )
