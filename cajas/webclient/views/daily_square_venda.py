import requests

from datetime import datetime, time, timedelta, date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.user import User
from cajas.concepts.models.concepts import Concept
from cajas.movement.models.movement_daily_square import MovementDailySquare
from cajas.office.models.officeCountry import OfficeCountry


class DailySquareVenda(LoginRequiredMixin, TemplateView):
    """Ver la caja de un usuario Cuadre diario
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_venda+.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareVenda, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        user = User.objects.get(pk=self.kwargs['pk'])
        box_daily_square = get_object_or_404(BoxDailySquare, user=user, office=office)
        withdraw_concept = get_object_or_404(Concept, name="Retiro unidad")
        investment_concept = get_object_or_404(Concept, name="Inversión Unidad")
        today = datetime.now().date() - timedelta(days=1)
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        total_withdraws = 0
        total_investments = 0
        withdraws_movements = MovementDailySquare.objects.filter(
            box_daily_square=box_daily_square,
            concept=withdraw_concept,
            date__lte=today_end,
            date__gte=today_start
        )
        investments_movements = MovementDailySquare.objects.filter(
            box_daily_square=box_daily_square,
            concept=investment_concept,
            date__lte=today_end,
            date__gte=today_start
        )
        withdraws_list = self.get_venda_withdraws(withdraws_movements, user)
        investments_list = self.get_venda_investments(investments_movements, user)
        withdraws_total = withdraws_movements.aggregate(Sum('value'))
        investments_total = investments_movements.aggregate(Sum('value'))
        if withdraws_total['value__sum']:
            total_withdraws = withdraws_total['value__sum']
        if investments_total['value__sum']:
            total_investments = investments_total['value__sum']
        context['box'] = box_daily_square
        context['office'] = office
        context['box_user'] = user
        context['withdraws'] = withdraws_movements
        context['investments'] = investments_movements
        context['withdraws_list'] = withdraws_list
        context['withdraws_list_total'] = self.get_venda_withdraws_total(withdraws_list)
        context['investments_list'] = investments_list
        context['investments_list_total'] = self.get_venda_investments_total(investments_list)
        context['withdraws_total'] = total_withdraws
        context['investments_total'] = total_investments
        return context

    def login(self):
        login = requests.get('http://external.vnmas.net/api/Session/Login/c184Ext/Gj7uQU')
        login = login.json()
        return login[0]['data'][0]['user']['token']

    def get_venda_withdraws(self, withdraws_movements, user):
        withdraws_list = list()
        now = date.today()
        today = now.strftime('%Y%m%d')
        yesterday = now - timedelta(days=1)
        yesterday = yesterday.strftime('%Y%m%d')
        token = self.login()
        for w in withdraws_movements:
            withdraws_venda = requests.get(
                'http://external.vnmas.net/api/Vmas/GetWithdrawals/{}/{}/{}/{}'.format(
                    token,
                    yesterday,
                    today,
                    w.unit.name,
                )
            )
            try:
                withdraws = withdraws_venda.json()
                if len(withdraws) > 0:
                    withdraws_values = withdraws[0]['data']
                    for i in withdraws_values:
                        withdraw = i['withdrawal']
                        if user.pk == int(withdraw['comment']):
                            values = dict()
                            values['route'] = withdraw['route']
                            values['date'] = withdraw['date']
                            values['comment'] = withdraw['comment']
                            values['value'] = withdraw['value']
                            withdraws_list.append(values)
            except Exception as e:
                print(e)
        return withdraws_list

    def get_venda_investments(self, investments_movements, user):
        investments_list = list()
        now = date.today()
        today = now.strftime('%Y%m%d')
        yesterday = now - timedelta(days=1)
        yesterday = yesterday.strftime('%Y%m%d')
        token = self.login()
        for i in investments_movements:
            investments = requests.get(
                'http://external.vnmas.net/api/Vmas/GetInvestments/{}/{}/{}/{}'.format(
                    token,
                    yesterday,
                    today,
                    i.unit.name,
                )
            )
            investments = investments.json()
            if len(investments) > 0:
                investments_values = investments[0]['data']
                for j in investments_values:
                    investment = j['investment']
                    if user.pk == int(investment['comment']):
                        values = dict()
                        values['route'] = investment['route']
                        values['date'] = investment['date']
                        values['comment'] = investment['comment']
                        values['value'] = investment['value']
                        investments_list.append(values)
        return investments_list

    def get_venda_withdraws_total(self, withdraws):
        total_withdraws = 0
        for w in withdraws:
            total_withdraws += int(w['value'])
        return total_withdraws

    def get_venda_investments_total(self, investments):
        total_investments = 0
        for i in investments:
            total_investments += int(i['value'])
        return total_investments
