
from rest_framework.generics import CreateAPIView
from ..models.supervisorCalendar import SupervisorCalendar
from ..serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer


class CreateSupervisorCalendar(CreateAPIView):
    queryset = SupervisorCalendar.objects.all()
    serializer_class = SupervisorCalendarSerializer
