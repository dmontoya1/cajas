
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View

from cajas.users.models.partner import Partner
from boxes.models.box_office import BoxOffice
from boxes.models.box_partner import BoxPartner
from concepts.models.concepts import Concept
from movement.models.movement_office import MovementOffice
from movement.models.movement_partner import MovementPartner
from office.models.office import Office


class Home(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        try:
            office = Office.objects.get(secretary=self.request.user.employee)
        except:
            office = None
        if office:
            context['office'] = office
        return context


class BoxDonJuanBox(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/donjuanbox.html'

    def get_context_data(self, **kwargs):
        context = super(BoxDonJuanBox, self).get_context_data(**kwargs)
        # try:
        #     office = Office.objects.get(secretary=self.request.user.employee)
        # except:
        #     office = None
        # if office:
        #     context['office'] = office
        return context


class PartnerList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partners_list.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerList, self).get_context_data(**kwargs)
        try:
            office = Office.objects.get(secretary=self.request.user.employee)
        except:
            office = None
        if office:
            partners = Partner.objects.filter(office=office, user__is_active=True)
            context['office'] = office
            context['partners'] = partners
        return context


class PartnerBox(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partner_box.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerBox, self).get_context_data(**kwargs)
        partner_pk = self.kwargs['pk']
        partner = Partner.objects.get(pk=partner_pk)
        try:
            box_partner = BoxPartner.objects.get(partner=partner)
        except:
            box_partner = None
        if box_partner:
            context['box'] = box_partner
        return context


class CreateOfficeMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        box_office = BoxOffice.objects.get(pk=request.user.employee.related_secretary_office.box.pk)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        movement = MovementOffice(
            box_office=box_office,
            concept=concept,
            date=date,
            movement_type=movement_type,
            value=value,
            detail=detail,
            responsible=request.user,
            ip=ip,

        )
        movement.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect('/')


class CreatePartnerMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        partner = Partner.objects.get(pk=request.POST['partner_id'])
        box_partner = BoxPartner.objects.get(partner=partner)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        movement = MovementPartner(
            box_partner=box_partner,
            concept=concept,
            date=date,
            movement_type=movement_type,
            value=value,
            detail=detail,
            responsible=request.user,
            ip=ip,
        )
        movement.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:partner-box', kwargs={'pk': request.POST['partner_id']}))

