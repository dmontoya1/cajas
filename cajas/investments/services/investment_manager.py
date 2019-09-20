
from django.shortcuts import get_object_or_404

from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.users.models.partner import Partner
from cajas.webclient.views.get_ip import get_ip

from ..models.investment import Investment
from ..models.investment_pay import InvestmentPay


class InvestmentManager(object):

    def investment_create(self, request):
        investment = self.create_object(request.data)
        data = request.data
        if int(data['initial_value']) > 0 and investment.investment_type == investment.BUSINESS:
            self.create_payment(request, investment)
            investment.balance = int(investment.balance) - int(request.data['initial_value_cop'])
            investment.save()

            concept = get_object_or_404(Concept, name='Inversión Negocios', concept_type=ConceptType.DOUBLE)
            data = {
                'partner': investment.partner,
                'box': investment.partner.box,
                'concept': concept,
                'movement_type': 'OUT',
                'value': request.data['initial_value'],
                'detail': "Pago cuota inicial {}".format(investment),
                'date': request.data['date'],
                'responsible': request.user,
                'ip': get_ip(request)
            }
            movement_partner_manager = MovementPartnerManager()
            return movement_partner_manager.create_double(data)
        return investment

    def create_object(self, data):
        investment = Investment.objects.create(
            partner=get_object_or_404(Partner, pk=data['partner']),
            date=data['date'],
            element=data['element'],
            total_value=data['total_value'],
            balance=data['total_value'],
            conditions=data['conditions'],
            initial_value=data['initial_value'],
            investment_type=data['investment_type']
        )
        return investment

    def create_payment(self, request, investment):
        InvestmentPay.objects.create(
            investment=investment,
            value=request.data['initial_value'],
            value_cop=request.data['initial_value_cop'],
            date=request.data['date'],
            detail="Pago cuota inicial {}".format(investment),
        )
