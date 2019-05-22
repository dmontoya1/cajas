
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.inventory.models import Category
from cajas.office.models.officeCountry import OfficeCountry
from cajas.office.models.officeItems import OfficeItems
from cajas.units.models.unitItems import UnitItems


class OfficeItemsList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/office_items_list.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeItemsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        unit_items = UnitItems.objects.filter(unit__partner__office=office)
        items = OfficeItems.objects.filter(office=office)
        categories = Category.objects.all()
        context['office'] = office
        context['items'] = items
        context['unit_items'] = unit_items
        context['categories'] = categories
        return context
