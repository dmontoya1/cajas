
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from office.models.officeCountry import OfficeCountry
from webclient.views.get_ip import get_ip

from ....models.movement_box_colombia import MovementBoxColombia
from ....services.box_colombia_service import MovementBoxColombiaManager
from ...serializers.movement_box_colombia_serializer import MovementBoxColombiaSerializer


class MovementBankColombiaCreate(generics.CreateAPIView):
    """
    """

    serializer_class = MovementBoxColombiaSerializer
    queryset = MovementBoxColombia.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        office = get_object_or_404(OfficeCountry, slug=self.kwargs['slug'])
        data['office'] = office
        data['ip'] = get_ip(request)
        data['responsible'] = request.user
        movement_box_colombia_manager = MovementBoxColombiaManager()
        movement_box_colombia_manager.create_bank_colombia_movement(data)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
