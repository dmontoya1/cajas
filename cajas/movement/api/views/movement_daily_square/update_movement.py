
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.concepts.models.concepts import Concept
from cajas.inventory.models.brand import Brand
from cajas.loans.services.loan_service import LoanManager
from cajas.office.models.officeCountry import OfficeCountry
from cajas.webclient.views.get_ip import get_ip
from cajas.webclient.views.utils import is_secretary

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
        data['pk'] = self.kwargs['pk']
        data['responsible'] = request.user
        data['ip'] = get_ip(request)
        concept = Concept.objects.get(pk=request.POST['concept'])
        office_country = OfficeCountry.objects.select_related('office', 'country', 'box').get(
            pk=request.session['office']
        )
        try:
            daily_square_manager.update_daily_square_movement(data)
            if concept.name == "Compra de Inventario Unidad":
                movement = get_object_or_404(MovementDailySquare, pk=kwargs['pk'])
                MovementDailySquareRequestItem.objects.filter(movement=movement).delete()
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
            elif concept.name == 'Préstamo empleado':
                movement = MovementDailySquare.objects.get(pk=data['pk'])
                loan_manager = LoanManager()
                value = data['value']
                if data['value'] == '':
                    value = data['loan_value']
                if request.user.is_superuser or is_secretary(request.user, office_country):
                    data_loan = {
                        'request': request,
                        'value': value,
                        'value_cop': 0,
                        'interest': data['interest'],
                        'time': data['time'],
                        'exchange': data['exchange'],
                        'office': request.session['office'],
                        'loan_type': 'EMP',
                        'lender': data['lender_employee'],
                        'box_from': data['box_from'],
                        'date': data['date'],
                    }
                    if data['box_from'] == 'partner':
                        data_loan['provider'] = data['partner_provider']
                    loan_manager.create_employee_loan(data_loan)
                    movement.review = True
                    movement.status = MovementDailySquare.APPROVED
                movement.save()
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
            'Se ha eliminado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
