from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.group import Group
from cajas.office.models.officeCountry import OfficeCountry
from .utils import is_secretary


class Groups(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/groups.html'

    def get_context_data(self, **kwargs):
        context = super(Groups, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        if self.request.user.is_superuser or is_secretary(self.request.user, office):
            context['employees'] = Employee.objects.filter(
                Q(office_country=office) |
                Q(office=office.office)
            ).order_by('user__first_name')
            context['admins'] = Employee.objects.filter(
                Q(office_country=office) |
                Q(office=office.office)
            ).order_by('user__first_name')
            existing_admins = Group.objects.filter(
                office=office
            )
        else:
            employee = Employee.objects.get(
                Q(user=self.request.user) & (Q(office=office.office) | Q(office_country=office))
            )
            existing_admins = Group.objects.filter(admin=employee, office=office)
        context['office'] = office
        context['existing'] = existing_admins

        return context
