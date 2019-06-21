
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.boxes.models import BoxDailySquare
from cajas.users.models.partner import Partner
from cajas.concepts.models.concepts import Concept
from cajas.core.services.email_service import EmailManager
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_withdraw import MovementWithdraw

User = get_user_model()
email_manager = EmailManager()


class MovementWithdrawRequestCreate(APIView):

    def post(self, request, format=None):
        if request.user.is_daily_square:
            self.create_movement_dq(request)
        else:
            self.create_movement_sec(request)
        email_manager.send_withdraw_email(request)
        return Response(
            'Se ha enviado la solicitud de retiro exitosamente',
            status=status.HTTP_201_CREATED
        )

    def create_movement_dq(self, request):
        partner = get_object_or_404(Partner, pk=request.data['partner'])
        concept = get_object_or_404(Concept, name="Retiro de Socio")
        box_daily = BoxDailySquare.objects.get(user=request.user, office=partner.office)
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

    def create_movement_sec(self, request):
        partner = get_object_or_404(Partner, pk=request.data['partner'])
        concept = get_object_or_404(Concept, name="Retiro de Socio")
        MovementWithdraw.objects.create(
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
