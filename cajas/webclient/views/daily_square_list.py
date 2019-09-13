import logging
from datetime import datetime

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models import BoxDailySquare
from cajas.general_config.models.exchange import Exchange
from cajas.inventory.models.category import Category
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.users.models import User, DailySquareUnits, Employee, Partner, GroupEmployee

from .utils import is_secretary, get_object_or_none, is_admin_senior

logger = logging.getLogger(__name__)


class DailySquareList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = OfficeCountry.objects.select_related('office').get(slug=slug)
        context['office'] = office
        offices = OfficeCountry.objects.select_related('office', 'country').all()
        users = User.objects.filter(Q(partner__office=office) | Q(related_employee__office_country=office) |
                                    Q(related_employee__office=office.office))
        units = Unit.objects.select_related(
            'partner',
            'collector',
            'supervisor'
        ).filter(
            Q(partner__office=office) | (Q(partner__code='DONJUAN') &
             (Q(collector__related_employee__office_country=office) |
             Q(collector__related_employee__office=office.office)
              ))).distinct()
        dq_list = User.objects.filter(
            (Q(partner__office=office) | Q(related_employee__office_country=office) |
             Q(related_employee__office=office.office)) &
            Q(is_daily_square=True)).distinct()
        context['dq_list'] = dq_list
        try:
            if self.request.user.is_superuser or is_secretary(self.request.user, office):
                context['dailys'] = User.objects.filter(
                    Q(is_daily_square=True) &
                    (Q(related_employee__office=office.office) |
                     Q(partner__office=office) |
                     Q(related_employee__office_country=office)
                     )
                ).distinct()
                dq_total = 0
                for dq in dq_list:
                    box, created = BoxDailySquare.objects.get_or_create(user=dq, office=office)
                    dq_total += box.balance
                context['dq_total'] = dq_total
            else:
                employee = Employee.objects.select_related('user', 'charge').get(
                    Q(user=self.request.user) & Q(office_country=office))
                groups = GroupEmployee.objects.select_related('group', 'supervisor', 'supervisor__user').filter(
                    Q(group__admin=employee) & Q(group__office=office)
                )
                if len(groups) > 0:
                    dailys = list()
                    for sup in groups:
                        if sup.supervisor.user.is_daily_square:
                            dailys.append(sup.supervisor.user)
                    if employee.user.is_daily_square and employee.user not in dailys:
                        dailys.append(employee.user)
                    context['dailys'] = dailys
                elif is_admin_senior(self.request.user, office):
                    context['dailys'] = User.objects.filter(
                        Q(is_daily_square=True) &
                        (Q(related_employee__office=office.office) |
                         Q(partner__office=office) |
                         Q(related_employee__office_country=office)
                         )
                    ).distinct()
                else:
                    context['dailys'] = User.objects.filter(pk=self.request.user.pk, is_daily_square=True)
                group_units = get_object_or_none(DailySquareUnits, employee=employee, employee__office_country=office)
                if group_units and group_units.units.all().exists():
                    units = group_units.units.filter(Q(partner__office=office) |
                                                     (Q(partner__code='DONJUAN') &
                                                      (Q(collector__related_employee__office_country=office) |
                                                       Q(collector__related_employee__office=office.office)
                                                       ))).distinct()
        except Exception as e:
            logger.exception(e)
            context['partner'] = Partner.objects.get(user=self.request.user, office=office)
        now = datetime.now()
        context['exchange'] = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=now.month,
        )
        context['categories'] = Category.objects.all()
        context['offices'] = offices
        context['units'] = units
        context['users'] = users

        return context
