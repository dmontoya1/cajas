
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from cajas.users.models.partner import Partner
from office.models.office import Office


class DailySquareList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        context['office'] = office
        try:
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['partners'] = Partner.objects.filter(
                    office=office,
                    user__is_active=True,
                    user__is_daily_square=True
                ).exclude(partner_type='DJ')
        except:
            context['partner'] = self.request.user.partner.get()

        return context
