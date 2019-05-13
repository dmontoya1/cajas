from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.group_employee import GroupEmployee
from cajas.users.models.group import Group
from cajas.office.models.officeCountry import OfficeCountry


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
        employees = Employee.objects.filter(
            Q(related_group_supervisor=None) &
            (Q(office_country=office) |
             Q(office=office.office))
        )
        admin = Employee.objects.filter(
            Q(group=None) &
            (Q(office_country=office) |
             Q(office=office.office))
        )
        existing_admins = Group.objects.filter(
            Q(admin__office=office.office) |
            Q(admin__office_country=office)
        )
        context['office'] = office
        context['admins'] = admin
        context['existing'] = existing_admins
        context['employees'] = employees

        return context
