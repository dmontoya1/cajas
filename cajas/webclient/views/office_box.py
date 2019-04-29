
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from inventory.models.category import Category
from office.models.officeCountry import OfficeCountry


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
        context['offices'] = OfficeCountry.objects.all()
        return context
