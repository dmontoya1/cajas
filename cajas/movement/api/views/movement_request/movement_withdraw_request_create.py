
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.users.models.partner import Partner
from concepts.models.concepts import Concept
from core.services.email_service import EmailManager
from webclient.views.get_ip import get_ip

from ....models.movement_withdraw import MovementWithdraw

User = get_user_model()
email_manager = EmailManager()


class MovementWithdrawRequestCreate(APIView):

    def post(self, request, format=None):
        self.create_movement(request)
        email_manager.send_withdraw_email(request)
        return Response(
            'Se ha enviado la solicitud de retiro exitosamente',
            status=status.HTTP_201_CREATED
        )

    def create_movement(self, request):
        partner = get_object_or_404(Partner, pk=request.data['partner'])
        concept = get_object_or_404(Concept, name="Retiro Socio")
        if request.user.related_daily_box:
            box_daily = request.user.related_daily_box.get()
        else:
            return Response(
                'No tienes permisos para realizar el retiro. Solo el cuadre diario puede hacer el retiro',
                status=status.HTTP_400_BAD_REQUEST
            )
        MovementWithdraw.objects.create(
            box_daily_square=box_daily,
            box_partner=partner.box,
            concept=concept,
            movement_type='OUT',
            value=request.data['value'],
            detail='Retiro de socio',
            date=datetime.now(),
            responsible=request.user,
            ip=get_ip(request),
            observation=request.data['observation'],
            withdraw_reason=request.data['message'],
        )
