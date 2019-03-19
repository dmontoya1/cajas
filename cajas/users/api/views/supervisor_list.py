from rest_framework.generics import ListAPIView

from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer


class SupervisorList(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self, *args, **kwargs):
        supervisor = Employee.objects.filter(office__pk=self.kwargs['pk'], charge__name="Supervisor")
        return supervisor
