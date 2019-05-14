
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.office.models.officeCountry import OfficeCountry


class OfficeColombia(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/office_colombia.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeColombia, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['box'] = get_object_or_404(BoxColombia, name='Caja Colombia')
        context['office'] = office
        context['offices'] = OfficeCountry.objects.all()

        return context
