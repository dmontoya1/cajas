
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxStatus
from cajas.inventory.models.category import Category
from cajas.users.models.partner import Partner
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit


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
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['partners'] = Partner.objects.filter(
                    office=office,
                    is_active=True,
                    box__box_status=BoxStatus.ABIERTA,
                ).exclude(partner_type='DJ')
            else:
                context['partner'] = Partner.objects.get(office=office, user=self.request.user)
        except Exception as e:
            context['partner'] = Partner.objects.get(office=office, user=self.request.user)

        context['categories'] = Category.objects.all()
        context['office'] = office
        context['units'] = units
        return context
