
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from chains.models.chain import Chain
from office.models.office import Office

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
        office = get_object_or_404(Office, slug=slug)
        chains = Chain.objects.filter(office=office)
        context['office'] = office
        context['chains'] = chains
        return context
