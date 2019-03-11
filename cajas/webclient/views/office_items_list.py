
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from inventory.models import Category
from office.models.office import Office
from office.models.officeItems import OfficeItems


class OfficeItemsList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/office_items_list.html'

    def get(self, request, slug):
        office = Office.objects.get(slug=slug)
        request.session['office'] = office.pk
        return super(OfficeItemsList, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(OfficeItemsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        items = OfficeItems.objects.filter(office__slug=slug)
        categories = Category.objects.all()
        context['office'] = office
        context['items'] = items
        context['categories'] = categories
        return context

