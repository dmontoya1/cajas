
from datetime import datetime

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.partner import Partner
from chains.models.user_place import UserPlace
from chains.models.chain_place import ChainPlace
from concepts.models.concepts import Concept
from investments.models.investment import Investment
from movement.models.movement_partner import MovementPartner
from movement.models.movement_don_juan import MovementDonJuan
from webclient.views.get_ip import get_ip


class PartnerCloseout(APIView):

    def post(self, request):
        self.validate_chains(request)
        self.validate_investments(request)

        return Response(
            "Se ha hecho la liquidación exitosamente.",
            status=status.HTTP_200_OK
        )

    def validate_chains(self, request):
        data = request.data
        partner = get_object_or_404(Partner, pk=data['partner'])
        partner_destiny = get_object_or_404(Partner, pk=data['partner_destiny'])
        office = partner.office
        today = datetime.now()
        user_places = UserPlace.objects.filter(user=partner.user)
        concept1 = get_object_or_404(Concept, name="Devolución Pago Cadenas")
        for place in user_places:
            chain = place.chain_place.chain
            pay_date = place.chain_place.pay_date
            if pay_date > today:
                payments = place.related_payments.all().aggregate(Sum('pay_value'))
                total = payments['pay_value__sum']
                MovementPartner.objects.create(
                    box_partner=partner.box,
                    concept=concept1,
                    movement_type='IN',
                    value=total,
                    detail='Devolución Pago puestos de la cadena {}'.format(place.chain_place.chain),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )
                if partner_destiny.code == 'DONJUAN':
                    MovementDonJuan.objects.create(
                        box_partner=BoxDonJuan.objects.filter(office=office),
                        concept=concept1.counterpart,
                        movement_type='OUT',
                        value=total,
                        detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
                else:
                    MovementPartner.objects.create(
                        box_partner=partner_destiny.box,
                        concept=concept1,
                        movement_type='OUT',
                        value=total,
                        detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
            else:
                month = datetime.now().month
                chain_places = place.chain_place.chain.places
                actual_place = ChainPlace.objects.get(chain=place.chain_place.chain, pay_date__month=month)
                actual_place = actual_place.name.split(" ")
                actual_place_number = actual_place[1]
                total_places = int(chain_places) - int(actual_place_number)
                concept2 = get_object_or_404(Concept, name="Pago Puestos Cadena")
                MovementPartner.objects.create(
                    box_partner=partner.box,
                    concept=concept2,
                    movement_type='OUT',
                    value=chain.place_value * total_places,
                    detail='Pagos puestos faltantes de la cadena {}'.format(place.chain_place.chain),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )
                MovementDonJuan.objects.create(
                    box_partner=BoxDonJuan.objects.filter(office=office),
                    concept=concept2.counterpart,
                    movement_type='IN',
                    value=chain.place_value * total_places,
                    detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )

            place.user = partner_destiny.user
            place.save()

    def validate_investments(self, request):
        data = request.data
        partner = get_object_or_404(Partner, pk=data['partner'])
        investments = Investment.objects.filter(partner=partner)
        for i in investments:
            if i.investment_type == Investment.BUSINESS:
                pass
