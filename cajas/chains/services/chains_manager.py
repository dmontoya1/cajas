
from datetime import datetime, date

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.partner import Partner
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry
from cajas.movement.models.movement_partner import MovementPartner
from cajas.movement.models.movement_don_juan import MovementDonJuan
from cajas.webclient.views.get_ip import get_ip
from ..models.chain import Chain
from ..models.chain_place import ChainPlace
from ..models.user_place import UserPlace
from ..models.user_place_pay import UserPlacePay


class ChainManager(object):

    def chain_manager(self, data):
        chain = self.create_chain(data)
        self.create_chain_places(data, chain)

    def create_chain(self, data):
        office = get_object_or_404(OfficeCountry, pk=int(data['office']))
        return Chain.objects.create(
            office=office,
            name=data['name'],
            places=data['places'],
            place_value=data['place_value'],
            chain_type=data['chain_type']
        )

    def create_chain_places(self, data, chain):
        places = int(data['places'])
        for i in range(1, places+1):
            place = ChainPlace.objects.create(
                chain=chain,
                name="Puesto {}".format(i),
                pay_date=data['pay_date_{}'.format(i)]
            )
            self.create_users_place(data, place, i)

    def create_users_place(self, data, place, i):
        counters = data['counters']
        for j in range(0, int(counters['counter_{}'.format(i)])):
            partner = get_object_or_404(Partner, pk=int(data['form[form][{}][partner_{}]'.format(j, i)]))
            UserPlace.objects.create(
                chain_place=place,
                user=partner.user,
                place_porcentaje=data['form[form][{}][place_porcentaje_{}]'.format(j, i)],
            )

    def get_partner_by_user_and_office(self, user, office):
        return Partner.objects.get(user=user, office=office)

    def create_chain_pay_partner_movement(self, data, user_place):
        try:
            concept = Concept.objects.get(name="Pago Puesto Cadena")
            partner = self.get_partner_by_user_and_office(user_place.user, data['office'])
            print(partner)
            MovementPartner.objects.create(
                box_partner=partner.box,
                concept=concept,
                movement_type='OUT',
                value=data['pay_value'],
                detail='Pagos puesto de la cadena {}'.format(user_place.chain_place.chain),
                date=datetime.now(),
                responsible=data['responsible'],
                ip=data['ip']
            )
            return True
        except Partner.DoesNotExist:
            return False

    def internal_chain_pay(self, data):
        user_place = UserPlace.objects.get(pk=data['user_place'])
        parter_payment = self.create_chain_pay_partner_movement(data, user_place)
        if parter_payment:
            UserPlacePay.objects.create(
                user_place=user_place,
                pay_value=data['pay_value'],
                date=data['date']
            )
            return True
        return False

    def user_place_update(self, request):
        data = request.data
        place = get_object_or_404(UserPlace, pk=data['user_place'])
        new_partner = get_object_or_404(Partner, code=data['code'])
        office = new_partner.office
        old_user = place.user
        old_partner = get_object_or_404(Partner, user=old_user, office=office)
        today = date.today()
        chain = place.chain_place.chain
        pay_date = place.chain_place.pay_date
        concept = get_object_or_404(Concept, name="Devolución Pago Cadenas")
        if old_partner != new_partner:
            if pay_date > today:
                payments = place.related_payments.all().aggregate(Sum('pay_value'))
                total = payments['pay_value__sum']
                if total:
                    MovementPartner.objects.create(
                        box_partner=old_partner.box,
                        concept=concept,
                        movement_type='IN',
                        value=total,
                        detail='Devolución Pago puestos de la cadena {}'.format(place.chain_place.chain),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
                    if data['code'] == 'DONJUAN':
                        MovementDonJuan.objects.create(
                            box_don_juan=BoxDonJuan.objects.get(office=office),
                            concept=concept.counterpart,
                            movement_type='OUT',
                            value=total,
                            detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                            date=datetime.now(),
                            responsible=request.user,
                            ip=get_ip(request)
                        )
                    else:
                        MovementPartner.objects.create(
                            box_partner=new_partner.box,
                            concept=concept.counterpart,
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
                    box_partner=old_partner.box,
                    concept=concept2,
                    movement_type='OUT',
                    value=chain.place_value * total_places,
                    detail='Pagos puestos faltantes de la cadena {}'.format(place.chain_place.chain),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )
                if data['code'] == 'DONJUAN':
                    MovementDonJuan.objects.create(
                        box_don_juan=BoxDonJuan.objects.get(office=office),
                        concept=concept2.counterpart,
                        movement_type='IN',
                        value=chain.place_value * total_places,
                        detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
                else:
                    MovementPartner.objects.create(
                        box_partner=new_partner.box,
                        concept=concept2.counterpart,
                        movement_type='IN',
                        value=chain.place_value * total_places,
                        detail='Pagos puestos de la cadena {}'.format(place.chain_place.chain),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )

            place.user = new_partner.user
            place.save()
