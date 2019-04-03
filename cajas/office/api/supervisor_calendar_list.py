from rest_framework.views import APIView
from django.http import JsonResponse

import datetime

from ..models.supervisorCalendar import SupervisorCalendar
from ..serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer


class SupervisorCalendarList(APIView):
    serializer_class = SupervisorCalendarSerializer

    def get(self, request, format=None):
        calendar = []
        if(request.user.employee.is_admin_charge()):
            super_calendar = SupervisorCalendar.objects.filter(
                office__slug=self.request.GET.get("office"),
                assigned_date__range=[
                    datetime.date.today() - datetime.timedelta(days=5),
                    datetime.date.today()
                ]
            )
        else:
            super_calendar = SupervisorCalendar.objects.filter(
                office__slug=self.request.GET.get("office"),
                supervisor=request.user
            )
        for item in super_calendar:
            scheduling = {}
            if item.assigned_date == datetime.date.today():
                scheduling["editable"] = True
            else:
                scheduling["editable"] = False
            scheduling["title"] = "Supervisor: {} \n Ruta: {} \n Socio: {} \n Cobrador: {}".format(
                item.supervisor.first_name + " " + item.supervisor.last_name,
                item.unit.name,
                item.unit.partner.user.first_name + " " + item.unit.partner.user.last_name,
                item.unit.collector.first_name + " " + item.unit.collector.last_name
            )
            scheduling["start"] = item.assigned_date
            scheduling["end"] = item.assigned_date
            scheduling["pk"] = item.pk
            calendar.append(scheduling)

        return JsonResponse(calendar, safe=False)
