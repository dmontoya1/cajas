
import logging

from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxStatus
from cajas.inventory.models.category import Category
from cajas.users.models import Partner, Employee
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit

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
        try:
            employee = Employee.objects.get(
                Q(user=self.request.user) & (Q(office=office.office) | Q(office_country=office)))
        except Employee.DoesNotExist:
            employee = None
        logger.exception(employee)
        try:
            if self.request.user.is_superuser or employee.is_admin_charge():
                logger.exception("Es Administrativo")
                context['partners'] = Partner.objects.filter(
                    office=office,
                    is_active=True,
                    box__box_status=BoxStatus.ABIERTA,
                ).exclude(partner_type='DJ')
            else:
                logger.exception("Else de es administrativo")
                context['partner'] = Partner.objects.get(office=office, user=self.request.user)
        except Exception as e:
            logger.exception("EXCEPTION EN PARTNER LIST")
            logger.exception(str(e))
            context['partner'] = Partner.objects.get(office=office, user=self.request.user)
        context['groups'] = Group.objects.all()
        context['categories'] = Category.objects.all()
        context['office'] = office
        context['units'] = units
        return context
