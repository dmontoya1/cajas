
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.office.models.officeCountry import OfficeCountry


class OfficeUSDBox(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/office_usd_box.html'

    def get(self, request, slug):
        office = OfficeCountry.objects.get(slug=slug)
        request.session['office'] = office.pk
        return super(OfficeUSDBox, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(OfficeUSDBox, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        context['offices'] = OfficeCountry.objects.select_related('office', 'country').all()
        context['box'] = BoxDonJuanUSD.objects.get(office=office)
        box_office = office.box
        if self.request.GET.get('all'):
            movements = box_office.movements.select_related('responsible', 'concept').all()
        else:
            movements = box_office.movements.select_related('responsible', 'concept').all()[:50]
        context['movements'] = movements
        return context
