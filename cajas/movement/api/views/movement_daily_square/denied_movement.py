from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication

from ....models import MovementDailySquare, MovementDonJuan, MovementDonJuanUsd, MovementPartner, MovementOffice
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem
from ....services.daily_square_service import MovementDailySquareManager
from ....services.utils import update_movements_balance, get_next_related_movement_by_date_and_pk, \
    update_movement_balance, update_all_movement_balance_on_update


class DeniedMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        if movement.concept.name == "Compra de Inventario Unidad" or movement.concept.name == "Compra ":
            MovementDailySquareRequestItem.objects.filter(movement=movement).delete()
        box = movement.box_daily_square
        movement.denied_detail = request.data['text']
        movement.review = True
        movement.status = MovementDailySquare.DENIED
        movement.detail += ' (RECHAZADO)'
        daily_square_manager = MovementDailySquareManager()
        update_movement_balance(movement, 0)
        if movement.movement_don_juan:
            update_movement_balance(
                movement.movement_don_juan,
                0
            )
            daily_square_manager.update_counterpart_movement_type(movement.movement_don_juan)
            related_movements = get_next_related_movement_by_date_and_pk(
                MovementDonJuan,
                'box_don_juan',
                movement.movement_don_juan.box_don_juan,
                movement.movement_don_juan.date,
                movement.movement_don_juan.pk
            )
            update_movements_balance(
                related_movements,
                movement.movement_don_juan.balance,
                movement.movement_don_juan.box_don_juan
            )
        if movement.movement_don_juan_usd:
            update_movement_balance(
                movement.movement_don_juan_usd,
                0
            )
            daily_square_manager.update_counterpart_movement_type(movement.movement_don_juan_usd)
            related_movements = get_next_related_movement_by_date_and_pk(
                MovementDonJuanUsd,
                'box_don_juan',
                movement.movement_don_juan_usd.box_don_juan,
                movement.movement_don_juan_usd.date,
                movement.movement_don_juan_usd.pk
            )
            update_movements_balance(
                related_movements,
                movement.movement_don_juan_usd.balance,
                movement.movement_don_juan_usd.box_don_juan
            )
        if movement.movement_partner:
            update_movement_balance(
                movement.movement_partner,
                0
            )
            daily_square_manager.update_counterpart_movement_type(movement.movement_partner)
            related_movements = get_next_related_movement_by_date_and_pk(
                MovementPartner,
                'box_partner',
                movement.movement_partner.box_partner,
                movement.movement_partner.date,
                movement.movement_partner.pk
            )
            update_movements_balance(
                related_movements,
                movement.movement_partner.balance,
                movement.movement_partner.box_partner
            )
        if movement.movement_office:
            update_movement_balance(
                movement.movement_office,
                0
            )
            daily_square_manager.update_counterpart_movement_type(movement.movement_office)
            related_movements = get_next_related_movement_by_date_and_pk(
                MovementOffice,
                'box_office',
                movement.movement_office.box_office,
                movement.movement_office.date,
                movement.movement_office.pk
            )
            update_movements_balance(
                related_movements,
                movement.movement_office.balance,
                movement.movement_office.box_office
            )
        if movement.movement_cd:
            update_movement_balance(
                movement.movement_cd,
                0
            )
            daily_square_manager.update_counterpart_movement_type(movement.movement_cd)
            related_movements = get_next_related_movement_by_date_and_pk(
                MovementDailySquare,
                'box_daily_square',
                movement.movement_cd.box_daily_square,
                movement.movement_cd.date,
                movement.movement_cd.pk
            )
            update_movements_balance(
                related_movements,
                movement.movement_cd.balance,
                movement.movement_cd.box_daily_square
            )
        movement.value = 0
        movement.save()
        update_all_movement_balance_on_update(
            MovementDailySquare,
            'box_daily_square',
            box,
            movement.date,
            movement.pk,
            movement
        )
        return Response(
            'El movimiento se ha rechazado exitosamente. No se creó ningún movimiento en otra caja',
            status=status.HTTP_201_CREATED
        )
