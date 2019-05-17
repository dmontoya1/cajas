
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxPartner
from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.office.models.officeCountry import OfficeCountry


class ArcRequest(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/arc_request.html'

    def get_context_data(self, **kwargs):
        context = super(ArcRequest, self).get_context_data(**kwargs)
        office = get_object_or_404(OfficeCountry, pk=self.request.session['office'])
        box_office = office.box
        box_donjuan = BoxDonJuan.objects.get(office=office)
        box_partners = BoxPartner.objects.filter(partner__office=office, is_active=True)
        box_partners_total = box_partners.aggregate(Sum('balance'))
        box_daily = BoxDailySquare.objects.filter(office=office)
        box_daily_total = box_daily.aggregate(Sum('balance'))
        dq_total = 0
        partner_sum = 0
        if box_daily_total['balance__sum'] is not None:
            dq_total = box_daily_total['balance__sum']
        if box_partners_total['balance__sum'] is not None:
            partner_sum = box_partners_total['balance__sum']
        partner_total = partner_sum + box_office.balance + box_donjuan.balance
        deficit = dq_total - partner_total
        context['office'] = office
        context['box_donjuan'] = box_donjuan
        context['box_office'] = box_office
        context['box_partners'] = box_partners
        context['box_daily'] = box_daily
        context['box_daily_total'] = dq_total
        context['partner_total'] = partner_total
        context['deficit'] = deficit
        return context
