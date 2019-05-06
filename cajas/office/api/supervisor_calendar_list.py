from rest_framework.views import APIView
from django.http import JsonResponse

import datetime

from django.shortcuts import get_object_or_404
from cajas.webclient.views.utils import get_object_or_none

from ..models.supervisorCalendar import SupervisorCalendar
from ..serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer
from cajas.users.models.group_employee import GroupEmployee
from cajas.users.models.group import Group
from cajas.users.models.employee import Employee


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
            if item.unit.partner:
                text += "\n Socio: {}".format(item.unit.partner.user.first_name + " " + item.unit.partner.user.last_name)
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
        calendar = []
        super_calendar = []
        try:
            user_type = request.user.related_employee.get()
        except:
            if request.user.is_superuser:
                super_calendar = SupervisorCalendar.objects.filter(
                    office__slug=self.request.GET.get("office"),
                    assigned_date__range=[
                        datetime.date.today() - datetime.timedelta(days=5),
                        datetime.date.today()
                    ]
                )
                calendar = get_calendar(super_calendar)
            else:
                calendar = []
            return JsonResponse(calendar, safe=False)

        if user_type.is_admin_charge():
            super_calendar = SupervisorCalendar.objects.filter(
                office__slug=self.request.GET.get("office"),
                assigned_date__range=[
                    datetime.date.today() - datetime.timedelta(days=5),
                    datetime.date.today()
                ]
            )
        elif str(user_type.charge) == "Administrador de Grupo":
            group = get_object_or_404(Group, admin=user_type)
            superv = GroupEmployee.objects.filter(
                group=group,
            )
            for i in superv:
                obj = SupervisorCalendar.objects.filter(supervisor=i.supervisor.user)
                for o in obj:
                    if obj is not None:
                        super_calendar.append(obj[0])
        elif str(user_type.charge) == "Supervisor":
            super_calendar = SupervisorCalendar.objects.filter(
                office__slug=self.request.GET.get("office"),
                supervisor=request.user
            )
        else:
            super_calendar = []

        calendar = get_calendar(super_calendar)
        return JsonResponse(calendar, safe=False)
