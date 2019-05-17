
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.partner import Partner
from cajas.chains.models.chain import Chain
from cajas.office.models.officeCountry import OfficeCountry

User = get_user_model()


class ChainList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/chain_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChainList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        chains_list = []
        partners = Partner.objects.filter(office=office)
        chains = Chain.objects.all()
        for p in partners:
            for c in chains:
                for cp in c.related_places.all():
                    for cu in cp.related_users.all():
                        if cu.user == p.user:
                            if c not in chains_list:
                                chains_list.append(c)

        context['office'] = office
        context['chains'] = chains_list
        return context
