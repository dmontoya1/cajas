
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.users.models.partner import Partner
from movement.api.views.CsrfExempt import CsrfExemptSessionAuthentication
from movement.models.movement_daily_square import MovementDailySquare
from movement.views.movement_partner.create_movement_service_simple import CreateMovementSimpleService
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare


class DispersionMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            movement = get_object_or_404(MovementDailySquare, pk=request.data['id'])
            counter = request.data['counter'] / 2
            counter = int(counter)
            for i in range(counter):
                value = request.data["form[form]["+str(i)+"][value]"]
                partner = get_object_or_404(Partner, pk=request.data["form[form]["+str(i)+"][partner]"])
                ip = get_ip(request)
                data = {
                    'box': partner.box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': value,
                    'detail': movement.detail,
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': ip
                }
                movement1 = CreateMovementSimpleService(data).call()

            movement.review = True
            movement.status = MovementDailySquare.DISPERSED
            movement.save()

            return Response(
                'El movimiento se ha dispersado de manera exitosa.',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                e,
                status=status.HTTP_400_BAD_REQUEST
            )
