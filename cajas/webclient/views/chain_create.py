
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.user import User
from cajas.office.models.officeCountry import OfficeCountry

User = get_user_model()


class ChainCreate(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/chain_create.html'

    def get_context_data(self, **kwargs):
        context = super(ChainCreate, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        context['users'] = User.objects.all().exclude(email="super@admin.com")
        context['offices'] = OfficeCountry.objects.all().order_by('slug')
        return context
