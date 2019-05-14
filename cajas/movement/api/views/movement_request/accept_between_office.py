from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.core.services.email_service import EmailManager
from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.users.models.employee import Employee


donjuan_manager = DonJuanManager()
email_manager = EmailManager()


class AcceptBetweenOfficeMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        movement = get_object_or_404(MovementBetweenOfficeRequest, pk=request.data['movement_id'])
        box_don_juan = get_object_or_404(BoxDonJuan, office=movement.box_office.office)
        data = {
            'box': box_don_juan,
            'concept': movement.concept.counterpart,
            'date': movement.date,
            'movement_type': movement.movement_type,
            'value': movement.value,
            'detail': movement.detail,
            'responsible': movement.responsible,
            'ip': movement.ip,
        }
        movement1 = donjuan_manager.create_movement(data)
        secretary = Employee.objects.filter(office=movement.box_office.office.office, charge__name='Secretaria').first()
        email_manager.send_office_mail(request, secretary.user.email)
        movement.delete()
        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
