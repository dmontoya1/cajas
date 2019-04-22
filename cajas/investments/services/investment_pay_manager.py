
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from concepts.models.concepts import Concept, ConceptType
from movement.services.partner_service import MovementPartnerManager
from webclient.views.get_ip import get_ip

from ..models.investment_pay import InvestmentPay
from ..models.investment import Investment

movement_partner_manager = MovementPartnerManager()
User = get_user_model()


class InvestmentPayManager(object):

    def add_payment(self, request):
        investment = get_object_or_404(Investment, pk=request.data['investment'])
        self.create_payment(request)
        investment.balance -= int(request.data['value'])
        investment.save()

        concept = get_object_or_404(Concept, name='Inversión Negocios', concept_type=ConceptType.SIMPLE)
        data = {
            'partner': investment.partner,
            'box': investment.partner.box,
            'concept': concept,
            'movement_type': 'OUT',
            'value': request.data['value'],
            'detail': request.data['detail'],
            'date': request.data['date'],
            'responsible': request.user,
            'ip': get_ip(request)
        }

        return movement_partner_manager.create_double(data)

    def create_payment(self, request):
        investment = get_object_or_404(Investment, pk=request.data['investment'])
        investment_pay = InvestmentPay.objects.create(
            investment=investment,
            value=request.data['value'],
            date=request.data['date'],
            detail=request.data['detail']
        )
