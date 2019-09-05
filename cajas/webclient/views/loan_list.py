
import logging
from datetime import datetime

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models import Partner, Employee, DailySquareUnits
from cajas.general_config.models.exchange import Exchange
from cajas.loans.models.loan import Loan, LoanType
from cajas.office.models.officeCountry import OfficeCountry
from .utils import get_object_or_none, is_secretary, is_admin_senior

User = get_user_model()
logger = logging.getLogger(__name__)


class LoanList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/loan_list.html'

    def get_context_data(self, **kwargs):
        context = super(LoanList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        try:
            employee = Employee.objects.get(
                Q(user=self.request.user) & Q(office_country=office))
        except Employee.DoesNotExist:
            employee = None
        try:
            group = get_object_or_none(DailySquareUnits, employee=employee)
        except:
            group = None

        if self.request.user.is_superuser or is_secretary(self.request.user, office) or \
            is_admin_senior(self.request.user, office):
            context['loans'] = Loan.objects.filter(office=office)
            context['partners'] = Partner.objects.filter(office=office, is_active=True)
            context['employees'] = Employee.objects.filter(
                Q(user__is_active=True) &
                (Q(office_country=office) | Q(office=office.office))
            )
            now = datetime.now()
            context['exchange'] = get_object_or_none(
                Exchange,
                currency=office.country.currency,
                month__month=now.month,
            )
        else:
            loans_list = list()
            if employee and group and self.request.user.groups.filter(name='Administrador de Grupo').exists():
                units = group.units.filter(Q(partner__office=office) |
                                           (Q(partner__code='DONJUAN') &
                                            (Q(collector__related_employee__office_country=office) |
                                             Q(collector__related_employee__office=office.office) |
                                             Q(supervisor__related_employee__office_country=office) |
                                             Q(supervisor__related_employee__office=office.office)
                                             ))).distinct()
                for u in units:
                    loans = Loan.objects.filter(
                        office=office,
                        lender=u.partner.user,
                    )
                    for loan in loans:
                        if loan not in loans_list:
                            loans_list.append(loan)
            elif employee and employee.user.groups.filter(name='Administrador de Grupo S.C').exists():
                loans = Loan.objects.filter(office=office, lender=self.request.user)
                partner = Partner.objects.get(office=office, user=self.request.user)
                for l in loans:
                    if l not in loans_list:
                        loans_list.append(l)
                mini_partners = Partner.objects.filter(direct_partner=partner)
                for mini_partner in mini_partners:
                    loans = Loan.objects.filter(
                        office=office,
                        lender=mini_partner.user,
                        loan_type=LoanType.SOCIO_DIRECTO
                    )
                    for loan in loans:
                        if loan not in loans_list:
                            loans_list.append(loan)
                context['loans'] = loans_list
            if self.request.user.groups.filter(name='Socios').exists():
                loans = Loan.objects.filter(office=office, lender=self.request.user)
                partner = Partner.objects.get(office=office, user=self.request.user)
                for l in loans:
                    if l not in loans_list:
                        loans_list.append(l)
                mini_partners = Partner.objects.filter(direct_partner=partner)
                for mini_partner in mini_partners:
                    loans = Loan.objects.filter(
                        office=office,
                        lender=mini_partner.user,
                        loan_type=LoanType.SOCIO_DIRECTO
                    )
                    for loan in loans:
                        if loan not in loans_list:
                            loans_list.append(loan)
                context['loans'] = loans_list
            else:
                context['loans'] = Loan.objects.filter(office=office, lender=self.request.user)
        context['office'] = office
        return context
