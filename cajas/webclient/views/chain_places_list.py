
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from chains.models.chain import Chain
from office.models.office import Office

User = get_user_model()


class ChainPlacesList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/chain_places_list.html'

    def get_context_data(self, **kwargs):
        context = super(ChainPlacesList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        chain = get_object_or_404(Chain, pk=self.kwargs['pk'])
        context['office'] = office
        context['chain'] = chain
        return context
