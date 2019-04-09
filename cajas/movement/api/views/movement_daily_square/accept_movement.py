
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication
from concepts.models.concepts import Concept, Relationship
from movement.services.office_service import MovementOfficeManager
from movement.services.partner_service import MovementPartnerManager
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare

movement_office_manager = MovementOfficeManager()
movement_partner_manager = MovementPartnerManager()


class AcceptMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        withdraw_concept = get_object_or_404(Concept, name="Retiro de Socio")
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        if movement.concept == withdraw_concept:
            data = {
                'box': movement.user.partner.get().box,
                'partner': movement.user.partner.get(),
                'value': movement.value,
                'detail': movement.detail,
                'date': movement.date,
                'responsible': request.user,
                'ip': get_ip(request)
            }
            movement_partner_manager.create_withdraw_movement(data)
        else:
            relationship = movement.concept.relationship
            if relationship == Relationship.UNIT:
                data = {
                    'box': movement.unit.partner.box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': movement.detail,
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                unit_movement = movement_partner_manager.create_simple(data)
            elif relationship == Relationship.PERSON:
                pass
            elif relationship == Relationship.OFFICE:
                data = {
                    'box': movement.office.box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': movement.detail,
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                office_movement = movement_office_manager.create_movement(data)
            elif relationship == Relationship.LOAN:
                pass
            elif relationship == Relationship.CHAIN:
                pass

        movement.review = True
        movement.status = MovementDailySquare.APPROVED
        movement.save()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
