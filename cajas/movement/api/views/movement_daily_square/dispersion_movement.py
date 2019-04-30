
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.partner import Partner
from api.CsrfExempt import CsrfExemptSessionAuthentication
from movement.models.movement_daily_square import MovementDailySquare
from movement.services.don_juan_service import DonJuanManager
from movement.services.partner_service import MovementPartnerManager
from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare


class DispersionMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        try:
            print("DISPERSION", request.data)
            movement = get_object_or_404(MovementDailySquare, pk=request.data['id'])
            counter = request.data['counter'] / 2
            counter = int(counter)
            for i in range(counter):
                value = request.data["form[form]["+str(i)+"][value]"]
                partner = get_object_or_404(Partner, pk=request.data["form[form]["+str(i)+"][partner]"])
                ip = get_ip(request)
                data = {
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': value,
                    'detail': movement.detail,
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': ip
                }
                if partner.code == 'DONJUAN':
                    don_juan_manager = DonJuanManager()
                    data['box'] = BoxDonJuan.objects.get(office__slug=request.data['office'])
                    don_juan_manager.create_movement(data)
                else:
                    data['box'] = partner.box
                    movement_partner_manager = MovementPartnerManager()
                    movement1 = movement_partner_manager.create_simple(data)

            movement.review = True
            movement.status = MovementDailySquare.DISPERSED
            movement.save()

            return Response(
                'El movimiento se ha dispersado de manera exitosa.',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(e)
            return Response(
                str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
