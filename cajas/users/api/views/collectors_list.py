from rest_framework.generics import ListAPIView

from cajas.users.models.employee import Employee
from cajas.users.api.serializers.employee_serilizer import EmployeeSerializer


class CollectorList(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self, *args, **kwargs):
        collectors = Employee.objects.filter(office__pk=self.kwargs['pk'], charge__name="Cobrador")
        return collectors
