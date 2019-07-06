
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.concepts.models.concepts import Concept
from cajas.inventory.models.brand import Brand
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare
from ....services.daily_square_service import MovementDailySquareManager
from ...serializers.movement_daily_square_serializer import MovementDailySquareSerializer
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem

logger = logging.getLogger(__name__)
daily_square_manager = MovementDailySquareManager()


class UpdateDailySquareMovement(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovementDailySquare.objects.all()
    serializer_class = MovementDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        print(self.kwargs['pk'])
        data['pk'] = self.kwargs['pk']
        data['responsible'] = request.user
        data['ip'] = get_ip(request)
        concept = Concept.objects.get(pk=request.POST['concept'])
        try:
            print("Go to update")
            daily_square_manager.update_daily_square_movement(data)
            print("Exit Update")
            if concept.name == "Compra de Inventario Unidad":
                movement = get_object_or_404(MovementDailySquare, pk=kwargs['pk'])
                items = MovementDailySquareRequestItem.objects.filter(movement=movement).delete()
                values = request.data["elemts"].split(",")
                for value in values:
                    if request.data["form[form][" + value + "][name]"] == '' or \
                    request.data["form[form][" + value + "][price]"] == '':
                        MovementDailySquareRequestItem.objects.create(
                            movement=movement,
                        )
                    else:
                        if "form[form][" + value + "][is_replacement]" in request.data:
                            MovementDailySquareRequestItem.objects.create(
                                movement=movement,
                                name=request.data["form[form][" + value + "][name]"],
                                brand=get_object_or_404(Brand, pk=request.data["form[form][" + value + "][brand]"]),
                                price=request.data["form[form][" + value + "][price]"],
                                is_replacement=True
                            )
                        else:
                            MovementDailySquareRequestItem.objects.create(
                                movement=movement,
                                name=request.data["form[form][" + value + "][name]"],
                                brand=get_object_or_404(Brand, pk=request.data["form[form][" + value + "][brand]"]),
                                price=request.data["form[form][" + value + "][price]"]
                            )
            return Response(
                'Se ha actualizado el movimiento exitosamente',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:

            logger.exception(str(e))
            print(e)
            return Response(
                'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                status=status.HTTP_204_NO_CONTENT
            )

    def delete(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']

        daily_square_manager.delete_daily_square_movement(data)
        return Response(
            'Se ha actualizado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
