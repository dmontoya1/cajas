from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..models.supervisorCalendar import SupervisorCalendar
from ..serializer.supervisor_calendar_serializer import SupervisorCalendarSerializer

from office.models.office import Office
from units.models.units import Unit

from django.shortcuts import get_object_or_404

User = get_user_model()


class CreateSupervisorCalendar(CreateAPIView):
    queryset = SupervisorCalendar.objects.all()
    serializer_class = SupervisorCalendarSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        SupervisorCalendar.objects.create(
            office=get_object_or_404(Office, pk=request.data["office"]),
            supervisor=get_object_or_404(User, pk=request.data["supervisor"]),
            unit=get_object_or_404(Unit, pk=request.data["unit"])
        )

        return Response(
            'Se ha creado el movimiento exitosamente.',
            status=status.HTTP_201_CREATED
        )
