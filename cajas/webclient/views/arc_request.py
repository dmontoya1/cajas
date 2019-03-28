
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from boxes.models.box_partner import BoxPartner
from boxes.models.box_daily_square import BoxDailySquare
from boxes.models.box_don_juan import BoxDonJuan
from office.models.office import Office


class ArcRequest(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/arc_request.html'

    def get_context_data(self, **kwargs):
        context = super(ArcRequest, self).get_context_data(**kwargs)
        office = get_object_or_404(Office, pk=self.request.session['office'])
        box_office = office.box
        box_donjuan = BoxDonJuan.objects.get(office=office)
        box_partners = BoxPartner.objects.filter(partner__office=office)
        box_partners_total = box_partners.aggregate(Sum('balance'))
        box_daily = BoxDailySquare.objects.filter(Q(user__partner__office=office) or Q(user_employee__office=office))
        box_daily_total = box_daily.aggregate(Sum('balance'))
        partner_total = box_partners_total['balance__sum'] + box_office.balance + box_donjuan.balance
        deficit = box_daily_total['balance__sum'] - partner_total
        context['office'] = office
        context['box_donjuan'] = box_donjuan
        context['box_office'] = box_office
        context['box_partners'] = box_partners
        context['box_daily'] = box_daily
        context['box_daily_total'] = box_daily_total['balance__sum']
        context['partner_total'] = partner_total
        context['deficit'] = deficit
        return context
