from rest_framework.views import APIView
from django.http import JsonResponse

import datetime

from cajas.office.models.supervisorCalendar import SupervisorCalendar
from cajas.office.api.serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer
from cajas.users.models.group_employee import GroupEmployee
from cajas.users.models.group import Group


def get_calendar(super_calendar):
    calendar = []
    for item in super_calendar:
        scheduling = {}
        if item.assigned_date == datetime.date.today():
            scheduling["editable"] = True
        else:
            scheduling["editable"] = False
        if item.unit:
            text = "Ruta: {}".format(item.unit.name)
            if item.supervisor:
                text += "\n Supervisor: {}".format(item.supervisor.first_name + " " + item.supervisor.last_name)
            if item.unit.collector:
                text += "\n Cobrador: {}".format(item.unit.collector.first_name + " " + item.unit.collector.last_name)
            scheduling["title"] = text
        else:
            scheduling["title"] = "Supervisor: {} \n Detalle: {}".format(
                item.supervisor.first_name + " " + item.supervisor.last_name,
                item.detail
            )
        scheduling["start"] = item.assigned_date
        scheduling["end"] = item.assigned_date
        scheduling["pk"] = item.pk
        calendar.append(scheduling)
    return calendar


class SupervisorCalendarList(APIView):

    serializer_class = SupervisorCalendarSerializer

    def get(self, request, format=None):
        super_calendar = []
        group = Group.objects.get(pk=self.request.GET.get('group'))
        superv = GroupEmployee.objects.filter(
            group=group,
        )
        for i in superv:
            obj = SupervisorCalendar.objects.filter(
                supervisor=i.supervisor.user,
                assigned_date__range=[
                    datetime.date.today() - datetime.timedelta(days=360),
                    datetime.date.today()
                ]
            )
            for o in obj:
                if o is not None:
                    super_calendar.append(o)
        calendar = get_calendar(super_calendar)
        return JsonResponse(calendar, safe=False)
