from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..models.supervisorCalendar import SupervisorCalendar
from ..serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer

from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit

from django.shortcuts import get_object_or_404

User = get_user_model()


class CreateSupervisorCalendar(CreateAPIView):
    queryset = SupervisorCalendar.objects.all()
    serializer_class = SupervisorCalendarSerializer

    def create(self, request, *args, **kwargs):
        if "unit" in request.data:
            unit = get_object_or_404(Unit, pk=request.data["unit"])
        else:
            unit = None
        SupervisorCalendar.objects.create(
            office=get_object_or_404(OfficeCountry, pk=request.data["office"]),
            supervisor=get_object_or_404(User, pk=request.data["supervisor"]),
            unit=unit,
            detail=request.data["detail"]
        )

        return Response(
            'Se ha creado el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
