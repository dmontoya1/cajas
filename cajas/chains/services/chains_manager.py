
from datetime import datetime, date

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry
from cajas.movement.models.movement_partner import MovementPartner
from cajas.movement.models.movement_don_juan import MovementDonJuan
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from cajas.webclient.views.get_ip import get_ip
from ..models.chain import Chain
from ..models.chain_place import ChainPlace
from ..models.user_place import UserPlace
from ..models.user_place_pay import UserPlacePay

movement_partner_manager = MovementPartnerManager()
don_juan_manager = DonJuanManager()


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
            user = get_object_or_404(User, pk=int(data['form[form][{}][partner_{}]'.format(j, i)]))
            UserPlace.objects.create(
                chain_place=place,
                user=user,
                office=OfficeCountry.objects.get(pk=int(data['form[form][{}][office_{}]'.format(j, i)])),
                place_porcentaje=data['form[form][{}][place_porcentaje_{}]'.format(j, i)],
            )

    def get_users_for_place_to_pay_chain(self, chain, month):
        place = ChainPlace.objects.get(
            chain=chain,
            pay_date__month=month
        )
        return place.related_users.all()

    def pay_month_chain_user(self, data, user):
        concept = Concept.objects.get(name="Pago Puesto Cadena")
        data_pay = {
            'concept': concept,
            'movement_type': 'IN',
            'value': data['value'],
            'detail': 'Pago cadena {}'.format(data['chain']),
            'date': datetime.now(),
            'responsible': data['responsible'],
            'ip': data['ip']
        }
        if user == 'DONJUAN':
            data_pay['box'] = BoxDonJuan.objects.get(office=data['office'])
            don_juan_manager.create_movement(data_pay)
        else:
            data_pay['box'] = data['partner'].box
            movement_partner_manager.create_simple(data_pay)

    def get_partner_by_user_and_office(self, user, office):
        return Partner.objects.get(user=user, office=office)

    def create_chain_pay_partner_movement(self, data, user_place):
        try:
            concept = Concept.objects.get(name="Pago Puesto Cadena")
            if int(user_place.user.document_id) == 1:
                data = {
                    'box': BoxDonJuan.objects.get(office=user_place.office),
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': data['pay_value'],
                    'detail': 'Pagos puesto de la cadena {}'.format(user_place.chain_place.chain),
                    'date': datetime.now(),
                    'responsible': data['responsible'],
                    'ip': data['ip']
                }
                don_juan_manager.create_movement(data)
            else:
                partner = self.get_partner_by_user_and_office(user_place.user, user_place.office)
                data = {
                    'box': partner.box,
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': data['pay_value'],
                    'detail': 'Pagos puesto de la cadena {}'.format(user_place.chain_place.chain),
                    'date': datetime.now(),
                    'responsible': data['responsible'],
                    'ip': data['ip']
                }
                movement_partner_manager.create_simple(data)
            return True
        except Partner.DoesNotExist:
            return False

    def internal_chain_pay(self, data):
        user_place = UserPlace.objects.get(pk=data['user_place'])
        partner_payment = self.create_chain_pay_partner_movement(data, user_place)
        print(partner_payment)
        if partner_payment:
            place_paid = UserPlacePay.objects.create(
                user_place=user_place,
                pay_value=data['pay_value'],
                date=data['date']
            )
            date_month = datetime.strptime(data['date'], "%Y-%m-%d").date()
            users_in_place = self.get_users_for_place_to_pay_chain(
                place_paid.user_place.chain_place.chain,
                date_month.month
            )
            for user_place in users_in_place:
                data_pay = {
                    'office': user_place.office,
                    'value': int(float(data['pay_value']) * user_place.place_porcentaje / float(100)),
                    'chain': user_place.chain_place.chain,
                    'responsible': data['responsible'],
                    'ip': data['ip']
                }

                if user_place.user.document_id == '1':
                    user_ = 'DONJUAN'
                else:
                    user_ = 'SOCIO'
                    data_pay['partner'] = self.get_partner_by_user_and_office(user_place.user, user_place.office)
                self.pay_month_chain_user(data_pay, user_)
            return True
        return False

    def user_place_update(self, request):
        data = request.data
        place = get_object_or_404(UserPlace, pk=data['user_place'])
        office = get_object_or_404(OfficeCountry, pk=data['office'])
        old_user = place.user
        new_user = get_object_or_404(User, pk=data['user'])
        if int(old_user.document_id) == 1:
            old_partner = Partner.objects.get(code='DONJUAN')
        elif place.office:
            old_partner = get_object_or_404(Partner, user=old_user, office=place.office)
        else:
            old_partner = None
        if int(new_user.document_id) == 1:
            new_partner = Partner.objects.get(code='DONJUAN')
        else:
            new_partner = get_object_or_404(Partner, user=new_user, office=office)
        today = date.today()
        chain = place.chain_place.chain
        pay_date = place.chain_place.pay_date
        concept = get_object_or_404(Concept, name="Devolución Pago Cadenas")
        if old_user != new_user:
            print("OLD USER difernte de NEW USER")
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
                    if old_partner.code == 'DONJUAN':
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
                if old_partner.code == 'DONJUAN':
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

            place.user = new_user
        place.office = office
        place.save()
