
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.boxes.models import BoxDonJuan, BoxOffice
from cajas.users.models.partner import Partner
from cajas.webclient.views.get_ip import get_ip
from cajas.office.models import OfficeCountry

from ....models.movement_daily_square import MovementDailySquare
from ....services.don_juan_service import DonJuanManager
from ....services.office_service import MovementOfficeManager
from ....services.partner_service import MovementPartnerManager


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
                ip = get_ip(request)
                value = request.data["form[form][" + str(i) + "][value]"]
                data = {
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': value,
                    'detail': movement.detail,
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': ip
                }
                print("form[form]["+str(i)+"][partner]")
                if request.data["form[form]["+str(i)+"][partner]"] == "office":
                    print("Entro al if")
                    office = OfficeCountry.objects.get(slug=request.data['office'])
                    office_manager = MovementOfficeManager()
                    data['box_office'] = BoxOffice.objects.get(office=office)
                    office_manager.create_movement(data)
                else:
                    print("ELSEEE")
                    partner = get_object_or_404(Partner, pk=request.data["form[form]["+str(i)+"][partner]"])

                    if partner.code == 'DONJUAN':
                        don_juan_manager = DonJuanManager()
                        data['box'] = BoxDonJuan.objects.get(office__slug=request.data['office'])
                        don_juan_manager.create_movement(data)
                    else:
                        data['box'] = partner.box
                        movement_partner_manager = MovementPartnerManager()
                        movement_partner_manager.create_simple(data)

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
