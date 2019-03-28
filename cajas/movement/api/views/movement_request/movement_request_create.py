
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from cajas.users.models.partner import Partner
from concepts.models.concepts import Concept
from core.services.email_service import EmailManager
from webclient.views.get_ip import get_ip

from ....models.movement_request import MovementRequest

User = get_user_model()
email_manager = EmailManager()


class MovementRequestCreate(APIView):

    def post(self, request, format=None):
        self.create_movement(request)
        email_manager.send_stop_email(request)
        return Response(
            'Se ha enviado la solicitud de aprobación exitosamente',
            status=status.HTTP_201_CREATED
        )

    def create_movement(self, request):
        try:
            request.data['partner_id']
            partner = get_object_or_404(Partner, pk=request.data['partner_id'])
        except MultiValueDictKeyError:
            user = get_object_or_404(User, pk=request.data['user'])
            partner = user.partner

        concept = get_object_or_404(Concept, pk=request.data['concept'])
        MovementRequest.objects.create(
            box_partner=partner.box,
            concept=concept,
            movement_type=request.data['movement_type'],
            value=request.data['value'],
            detail=request.data['detail'],
            date=request.data['date'],
            responsible=request.user,
            ip=get_ip(request),
            observation=request.data['observation']
        )
