
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.core.services.email_service import EmailManager
from cajas.movement.models import MovementDonJuan, MovementBoxColombia
from cajas.users.models import Employee

from ....models.movement_between_office_request import MovementBetweenOfficeRequest


class DeclineBetweenOfficeMovement(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        movement = get_object_or_404(
            MovementBetweenOfficeRequest,
            pk=request.data['movement_id']
        )
        if movement.from_box_type == MovementBetweenOfficeRequest.BOX_DON_JUAN:
            origin_movement = MovementDonJuan.objects.get(pk=movement.origin_movement_pk)
            secretary = Employee.objects.filter(
                office=origin_movement.box_don_juan.office.office,
                charge__name='Secretaria'
            ).first()
            email_to = secretary.user.email
        elif movement.from_box_type == MovementBetweenOfficeRequest.BOX_COLOMBIA:
            origin_movement = MovementBoxColombia.objects.get(pk=movement.origin_movement_pk)
            email_to = "nfcinversiones@hotmail.com"
        email_manager = EmailManager()
        email_manager.send_denied_between_office_movement_email(request, origin_movement, email_to)
        origin_movement.delete()
        movement.delete()
        return Response(
            'El movimiento se ha rechazo exitosamente. No se ha creado el movimiento en la caja',
            status=status.HTTP_201_CREATED
        )
