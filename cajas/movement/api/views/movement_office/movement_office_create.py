
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.office.models.officeCountry import OfficeCountry
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_office import MovementOffice
from ....services.office_service import MovementOfficeManager
from ...serializers.movement_office_serializer import MovementOfficeSerializer


class MovementOfficeCreate(generics.CreateAPIView):
    """
    """

    serializer_class = MovementOfficeSerializer
    queryset = MovementOffice.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        office = get_object_or_404(OfficeCountry, slug=self.kwargs['slug'])
        data['office'] = office
        data['ip'] = get_ip(request)
        data['responsible'] = request.user
        movement_office_manager = MovementOfficeManager()
        movement_office_manager.create_office_movement(data)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
