
from datetime import datetime, date

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_partner import BoxStatus
from cajas.users.models.partner import Partner, PartnerType
from chains.models.user_place import UserPlace
from chains.models.chain_place import ChainPlace
from concepts.models.concepts import Concept, ConceptType
from investments.models.investment import Investment
from loans.models.loan import Loan, LoanType
from loans.models.loan_payments import LoanPayment
from movement.models.movement_partner import MovementPartner
from movement.models.movement_don_juan import MovementDonJuan
from webclient.views.get_ip import get_ip


class PartnerCloseout(APIView):

    def post(self, request):
        total = 0
        self.validate_chains(request)
        self.validate_investments(request)
        self.validate_loans(request)
        self.generate_closeout(request)
        partner = get_object_or_404(Partner, pk=request.data['partner'])
        if partner.box.balance > 0:
            total = partner.box.balance
        return Response(
            "Se ha hecho la liquidación exitosamente. El valor final de la caja del socio es ${}".format(total),
            status=status.HTTP_200_OK
        )

    def validate_chains(self, request):
        data = request.data
        partner = get_object_or_404(Partner, pk=data['partner'])
        partner_destiny = get_object_or_404(Partner, code=data['partner_destiny'])
        office = partner.office
        today = date.today()
        user_places = UserPlace.objects.filter(user=partner.user)
        concept1 = get_object_or_404(Concept, name="Devolución Pago Cadenas")
        for place in user_places:
            chain = place.chain_place.chain
            pay_date = place.chain_place.pay_date
            if pay_date > today:
                payments = place.related_payments.all().aggregate(Sum('pay_value'))
                total = payments['pay_value__sum']
                if total:
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
                            concept=concept1.counterpart,
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
        office = partner.office
        investments = Investment.objects.filter(partner=partner)
        concept = Concept.objects.get(name="Inversión Negocios", concept_type=ConceptType.DOUBLE)
        for i in investments:
            if i.investment_type == Investment.BUSINESS:
                pays = i.related_pays.all().aggregate(Sum('value'))
                if pays['value__sum']:
                    MovementPartner.objects.create(
                        box_partner=partner.box,
                        concept=concept,
                        movement_type='IN',
                        value=pays['value__sum'],
                        detail='Devolución Pagos inversión {}'.format(i),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)

                    )
                    MovementDonJuan.objects.create(
                        box_partner=BoxDonJuan.objects.filter(office=office),
                        concept=concept.counterpart,
                        movement_type='OUT',
                        value=pays['value__sum'],
                        detail='Devolución Pagos inversión {} al socio {}'.format(i, partner),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )

    def validate_loans(self, request):
        data = request.data
        partner = get_object_or_404(Partner, pk=data['partner'])
        office = partner.office
        loans = Loan.objects.filter(lender=partner.user)
        for loan in loans:
            if loan.loan_type == LoanType.EMPLEADO:
                if loan.balance > 0:
                    concept = Concept.objects.get(name='Pago Abono préstamo socio')
                    MovementPartner.objects.create(
                        box_partner=partner.box,
                        concept=concept,
                        movement_type='OUT',
                        value=loan.balance * 3,
                        detail='Pago préstamo por ${} (Sale como retiro de socio)'.format(loan.balance),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
                    if partner.partner_type == PartnerType.DIRECTO:
                        MovementDonJuan.objects.create(
                            box_partner=BoxDonJuan.objects.filter(office=office),
                            concept=concept.counterpart,
                            movement_type='IN',
                            value=loan.balance * 3,
                            detail='Pago préstamo por ${} (Entra como retiro de socio)'.format(loan.balance),
                            date=datetime.now(),
                            responsible=request.user,
                            ip=get_ip(request)
                        )
                    else:
                        MovementPartner.objects.create(
                            box_partner=partner.direct_partner.box,
                            concept=concept.counterpart,
                            movement_type='IN',
                            value=loan.balance * 3,
                            detail='Pago préstamo por ${} (Entra como retiro de socio)'.format(loan.balance),
                            date=datetime.now(),
                            responsible=request.user,
                            ip=get_ip(request)
                        )
                    LoanPayment.objects.create(
                        loan=loan,
                        value=loan.balance,
                        date=datetime.now()
                    )
            elif loan.loan_type == LoanType.SOCIO_DIRECTO:
                if loan.balance > 0:
                    concept = Concept.objects.get(name='Pago Abono préstamo socio')
                    MovementPartner.objects.create(
                        box_partner=partner.box,
                        concept=concept,
                        movement_type='OUT',
                        value=loan.balance,
                        detail='Pago préstamo por ${}'.format(loan.balance),
                        date=datetime.now(),
                        responsible=request.user,
                        ip=get_ip(request)
                    )
                    if partner.partner_type == PartnerType.DIRECTO:
                        MovementDonJuan.objects.create(
                            box_partner=BoxDonJuan.objects.filter(office=office),
                            concept=concept.counterpart,
                            movement_type='IN',
                            value=loan.balance,
                            detail='Pago préstamo por ${}'.format(loan.balance),
                            date=datetime.now(),
                            responsible=request.user,
                            ip=get_ip(request)
                        )
                    else:
                        MovementPartner.objects.create(
                            box_partner=partner.direct_partner.box,
                            concept=concept.counterpart,
                            movement_type='IN',
                            value=loan.balance,
                            detail='Pago préstamo por ${}'.format(loan.balance),
                            date=datetime.now(),
                            responsible=request.user,
                            ip=get_ip(request)
                        )
                    LoanPayment.objects.create(
                        loan=loan,
                        value=loan.balance,
                        date=datetime.now()
                    )

    def generate_closeout(self, request):
        partner = get_object_or_404(Partner, pk=request.data['partner'])
        box = partner.box
        balance = box.balance
        if box.balance > 0:
            concept = Concept.objects.get(name="Liquidación Sociedad")
            MovementPartner.objects.create(
                box_partner=partner.box,
                concept=concept,
                movement_type='OUT',
                value=(balance / 3) * 2,
                detail='Liquidación sociedad',
                date=datetime.now(),
                responsible=request.user,
                ip=get_ip(request)
            )
            if partner.partner_type == PartnerType.DIRECTO:
                MovementDonJuan.objects.create(
                    box_partner=BoxDonJuan.objects.filter(office=partner.office),
                    concept=concept.counterpart,
                    movement_type='IN',
                    value=(balance / 3) * 2,
                    detail='Liquidación Socio {}'.format(partner),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )
            else:
                MovementPartner.objects.create(
                    box_partner=partner.direct_partner.box,
                    concept=concept.counterpart,
                    movement_type='IN',
                    value=(balance / 3) * 2,
                    detail='Liquidación Socio {}'.format(partner),
                    date=datetime.now(),
                    responsible=request.user,
                    ip=get_ip(request)
                )
            box.box_status = BoxStatus.EN_LIQUIDACION
        else:
            box.box_status = BoxStatus.LIQUIDADA
        partner.is_active = False
        partner.save()
        box.save()
