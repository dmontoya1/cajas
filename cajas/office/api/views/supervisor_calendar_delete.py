from rest_framework import generics 

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.office.models.supervisorCalendar import SupervisorCalendar
from cajas.office.api.serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer


class SupervisorCalendarDelete(generics.DestroyAPIView):
    queryset = SupervisorCalendar.objects.all()
    serializer_class = SupervisorCalendarSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
