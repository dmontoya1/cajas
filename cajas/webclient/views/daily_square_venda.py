from datetime import datetime, time, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.user import User
from concepts.models.concepts import Concept
from movement.models.movement_daily_square import MovementDailySquare
from office.models.officeCountry import OfficeCountry


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
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        total_withdraws = 0
        total_investments = 0
        withdraws = MovementDailySquare.objects.filter(
            box_daily_square=box_daily_square,
            concept=withdraw_concept,
            date__lte=today_end,
            date__gte=today_start
        )
        investments = MovementDailySquare.objects.filter(
            box_daily_square=box_daily_square,
            concept=investment_concept,
            date__lte=today_end,
            date__gte=today_start
        )
        withdraws_total = withdraws.aggregate(Sum('value'))
        investments_total = investments.aggregate(Sum('value'))
        if withdraws_total['value__sum']:
            total_withdraws = withdraws_total['value__sum']
        if investments_total['value__sum']:
            total_investments = investments_total['value__sum']
        context['box'] = box_daily_square
        context['office'] = office
        context['box_user'] = user
        context['withdraws'] = withdraws
        context['investments'] = investments
        context['withdraws_total'] = total_withdraws
        context['investments_total'] = total_investments
        return context
