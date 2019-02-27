
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.partner import Partner
from office.models.office import Office


class PartnerList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partners_list.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerList, self).get_context_data(**kwargs)
        office = get_object_or_404(Office, secretary=self.request.user.employee)
        partners = Partner.objects.filter(office=office, user__is_active=True).exclude(partner_type='DJ')
        context['office'] = office
        context['partners'] = partners
        return context
