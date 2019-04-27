
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.CsrfExempt import CsrfExemptSessionAuthentication
from concepts.models.concepts import Concept, Relationship
from movement.services.office_service import MovementOfficeManager
from movement.services.partner_service import MovementPartnerManager
from units.models.unitItems import UnitItems
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem

movement_office_manager = MovementOfficeManager()
movement_partner_manager = MovementPartnerManager()


class AcceptMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        withdraw_concept = get_object_or_404(Concept, name="Retiro de Socio")
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        user = movement.box_daily_square.user
        if movement.concept == withdraw_concept:
            data = {
                'box': movement.user.partner.get().box,
                'partner': movement.user.partner.get(),
                'value': movement.value,
                'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
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
                    'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                unit_movement = movement_partner_manager.create_simple(data)
                movement.movement_partner = unit_movement
            elif relationship == Relationship.PERSON:
                data = {
                    'box': movement.user.partner.get().box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                movement_person = movement_partner_manager.create_simple(data)
                movement.movement_partner = movement_person
            elif relationship == Relationship.OFFICE:
                data = {
                    'box': movement.office.box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                office_movement = movement_office_manager.create_movement(data)
                movement.movement_office = office_movement
            elif relationship == Relationship.LOAN:
                pass
            elif relationship == Relationship.CHAIN:
                pass
        if movement.concept.name == "Compra de Inventario Unidad":
            movement_items = MovementDailySquareRequestItem.objects.filter(
                movement=movement
            )
            for item in movement_items:
                if not item.name or not item.price or not item.brand:
                    return Response(
                        'Debe crearse el inventario de la unidad para aprobar el movimiento',
                        status=status.HTTP_206_PARTIAL_CONTENT
                    )
                else:
                    item_create = UnitItems()
                    item_create.name = item.name
                    item_create.price = item.price
                    item_create.brand = item.brand
                    print(item.movement.unit)
                    print(item.movement.office)
                    if item.movement.unit:
                        item_create.unit = item.movement.unit
                    else:
                        item_create.unit = item.movement.office
                    if item.is_replacement:
                        item_create.is_replacement = True
                    item_create.save()
                    print(item_create.office)
                    print(item_create.name)
                    print(item_create.unit)
                    print(item_create.is_replacement)
            movement_items.delete()
        movement.review = True
        movement.status = MovementDailySquare.APPROVED
        movement.save()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
