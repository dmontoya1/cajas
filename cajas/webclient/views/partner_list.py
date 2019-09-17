import logging

from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxStatus
from cajas.inventory.models.category import Category
from cajas.users.models import Partner, Employee, DailySquareUnits
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit

from .utils import get_object_or_none, is_secretary, is_admin_senior
logger = logging.getLogger(__name__)


class PartnerList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partners_list.html'

    def get(self, request, slug):
        office = OfficeCountry.objects.get(slug=slug)
        request.session['office'] = office.pk
        return super(PartnerList, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(PartnerList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        units = Unit.objects.filter(partner__office=office)
        if not self.request.user.is_superuser:
            try:
                employee = Employee.objects.get(
                    Q(user=self.request.user), (Q(office_country=office) | Q(office=office.office))
                )
            except Exception as e:
                employee = None
            group = get_object_or_none(DailySquareUnits, employee=employee, employee__office_country=office)
            context['employee'] = employee
            if is_secretary(self.request.user, office) or is_admin_senior(self.request.user, office):
                context['partners'] = Partner.objects.filter(
                    office=office,
                    is_active=True,
                    box__box_status=BoxStatus.ABIERTA,
                ).exclude(partner_type='DJ')
            else:
                partners = list()
                try:
                    partner = Partner.objects.get(office=office, user=self.request.user)
                except:
                    partner = None
                if employee and group and employee.user.groups.filter(name='Administrador de Grupo').exists():
                    units = group.units.filter(Q(partner__office=office) |
                                               (Q(partner__code='DONJUAN') &
                                                (Q(collector__related_employee__office_country=office) |
                                                 Q(collector__related_employee__office=office.office) |
                                                 Q(supervisor__related_employee__office_country=office) |
                                                 Q(supervisor__related_employee__office=office.office)
                                                 ))).distinct()
                    for u in units:
                        if u.partner not in partners:
                            partners.append(u.partner)
                elif employee and employee.user.groups.filter(name='Administrador de Grupo S.C').exists():
                    logger.exception("El user tiene Admin de Grupo Sin Caja")
                    if partner not in partners:
                        partners.append(partner)
                    mini_partners = Partner.objects.filter(direct_partner=partner)
                    for p in mini_partners:
                        if p not in partners:
                            partners.append(p)
                    logger.exception("Lista de socios", partners)
                if self.request.user.groups.filter(name='Socios').exists():
                    if partner not in partners:
                        partners.append(partner)
                    mini_partners = Partner.objects.filter(direct_partner=partner)
                    for p in mini_partners:
                        if p not in partners:
                            partners.append(p)
                context['partner'] = partners
        else:
            context['partners'] = Partner.objects.filter(
                office=office,
                is_active=True,
                box__box_status=BoxStatus.ABIERTA,
            ).exclude(partner_type='DJ')
        context['groups'] = Group.objects.all()
        context['categories'] = Category.objects.all()
        context['office'] = office
        context['units'] = units
        return context
