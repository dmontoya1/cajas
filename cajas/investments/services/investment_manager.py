
from django.shortcuts import get_object_or_404

from cajas.users.models.partner import Partner
from ..models.investment import Investment
from ..services.investment_pay_manager import InvestmentPayManager

pay_manager = InvestmentPayManager()


class InvestmentManager(object):

    def investment_create(self, data):
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
        if investment.initial_value > 0:
            data1 = {
                'investment': investment,
                'date': investment.date,
                'value': investment.initial_value
            }
            pay_manager.add_payment(data1)
        return investment
