
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication
from concepts.models.concepts import Relationship
from movement.views.movement_partner.create_movement_service_simple import CreateMovementSimpleService
from movement.views.movement_country.create_movement import CreateMovementCountry
from movement.views.movement_office.create_movement import CreateMovementOffice
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare


class AcceptMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
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
            unit_movement = CreateMovementSimpleService(data).call()
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
            office_movement = CreateMovementOffice(data).call()
        elif relationship == Relationship.LOAN:
            pass
        elif relationship == Relationship.COUNTRY:
            data = {
                'box': movement.country.box,
                'concept': movement.concept,
                'movement_type': movement.movement_type,
                'value': movement.value,
                'detail': movement.detail,
                'date': movement.date,
                'responsible': request.user,
                'ip': get_ip(request)
            }
            country_movement = CreateMovementCountry(data).call()
        elif relationship == Relationship.CHAIN:
            pass

        movement.review = True
        movement.status = MovementDailySquare.APPROVED
        movement.save()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
