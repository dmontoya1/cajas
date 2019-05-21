
from datetime import datetime

from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models import BoxDailySquare
from cajas.general_config.models.exchange import Exchange
from cajas.inventory.models.category import Category
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.users.models.user import User
from cajas.webclient.views.utils import get_object_or_none


class DailySquareList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        offices = OfficeCountry.objects.all()
        units = Unit.objects.filter(partner__office=office)
        users = User.objects.filter(Q(partner__office=office) | Q(related_employee__office_country=office) |
                                    Q(related_employee__office=office.office))
        try:
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['dailys'] = User.objects.filter(
                    Q(is_daily_square=True) &
                    (Q(related_employee__office=office.office) |
                     Q(partner__office=office) |
                     Q(related_employee__office_country=office)
                     )
                ).distinct()
            else:
                context['dailys'] = User.objects.filter(pk=self.request.user.pk, is_daily_square=True)
        except Exception as e:
            print(e)
            context['partner'] = self.request.user.partner.get()
        dq_list = User.objects.filter(
            (Q(partner__office=office) | Q(related_employee__office_country=office) |
             Q(related_employee__office=office.office)) &
            Q(is_daily_square=True)).distinct()
        now = datetime.now()
        context['exchange'] = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=now.month,
        )
        dq_total = 0
        for dq in dq_list:
            box = BoxDailySquare.objects.get(user=dq, office=office)
            dq_total += box.balance
        context['dq_total'] = dq_total
        context['dq_list'] = dq_list
        context['categories'] = Category.objects.all()
        context['offices'] = offices
        context['units'] = units
        context['users'] = users

        return context
