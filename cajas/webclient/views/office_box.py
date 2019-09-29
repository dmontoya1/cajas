
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.inventory.models.category import Category
from cajas.office.models.officeCountry import OfficeCountry


class OfficeBox(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    permission_required = 'boxes.change_boxoffice'
    template_name = 'webclient/office_box.html'

    def get(self, request, slug):
        office = OfficeCountry.objects.get(slug=slug)
        request.session['office'] = office.pk
        return super(OfficeBox, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(OfficeBox, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        context['categories'] = Category.objects.all()
        context['offices'] = OfficeCountry.objects.select_related('office', 'country').all()
        box_office = office.box
        if self.request.GET.get('all'):
            movements = box_office.movements.select_related('responsible', 'concept').all()
        else:
            movements = box_office.movements.select_related('responsible', 'concept').all()[:50]
        context['movements'] = movements
        return context
