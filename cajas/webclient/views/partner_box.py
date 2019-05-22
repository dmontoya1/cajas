
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import Partner
from cajas.inventory.models.category import Category
from cajas.office.models.officeCountry import OfficeCountry


class PartnerBox(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partner_box.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerBox, self).get_context_data(**kwargs)
        partner_pk = self.kwargs['pk']
        partner = Partner.objects.get(pk=partner_pk)
        box_partner = get_object_or_404(BoxPartner, partner=partner)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['categories'] = Category.objects.all()
        context['office'] = office
        context['box'] = box_partner
        return context
