
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from boxes.models.box_daily_square import BoxDailySquare
from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_office import BoxOffice
from boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from concepts.models.concepts import Concept, ConceptType, CrossoverType
from movement.models.movement_daily_square import MovementDailySquare
from movement.models.movement_office import MovementOffice
from movement.models.movement_partner import MovementPartner
from movement.views.movement_partner.movement_partner import MovementPartner as MovementPartnerHandler
from movement.views.movement_don_juan.movement_don_juan import MovementDonJuan
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


class BoxDonJuanOffice(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/donjuanbox.html'

    def get_context_data(self, **kwargs):
        context = super(BoxDonJuanOffice, self).get_context_data(**kwargs)
        concepts = Concept.objects.filter(is_active=True)
        try:
            office = Office.objects.get(secretary=self.request.user.employee)
        except:
            office = None
        if office:
            box = BoxDonJuan.objects.get(office=office)
            context['box'] = box
        context['concepts'] = concepts
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
            partners = Partner.objects.filter(office=office, user__is_active=True).exclude(partner_type='DJ')
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


class PartnerCreate(LoginRequiredMixin, View):
    """
    """

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        document_type = request.POST['document_type']
        document_id = request.POST['document_id']
        partner_type = request.POST['partner_type']
        try:
            direct_partner = Partner.objects.get(pk=request.POST['direct_partner'])
        except:
            direct_partner = None
        initial_value = request.POST['initial_value']
        try:
            request.POST['daily_square']
            daily_square = True
        except:
            daily_square = False
        office = Office.objects.get(pk=request.POST['office'])
        user = User(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name,
            document_type=document_type,
            document_id=document_id
        )
        user.save()

        partner = Partner(
            user=user,
            office=office,
            partner_type=partner_type,
            direct_partner=direct_partner,
            is_daily_square=daily_square
        )
        partner.save()
        if int(initial_value) > 0:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            movement = MovementPartnerHandler.create_partner_movements(
                partner,
                initial_value,
                request.user,
                ip
            )
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el socio exitosamente')
        return HttpResponseRedirect(reverse('webclient:partners_list'))


class DailySquareList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareList, self).get_context_data(**kwargs)
        try:
            office = Office.objects.get(secretary=self.request.user.employee)
        except:
            office = None
        if office:
            partners = Partner.objects.filter(office=office, user__is_active=True, is_daily_square=True).exclude(partner_type='DJ')
            context['office'] = office
            context['partners'] = partners
        return context


class DailySquareBox(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_box.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareBox, self).get_context_data(**kwargs)
        user_pk = self.kwargs['pk']
        user = User.objects.get(pk=user_pk)
        try:
            box_daily_square = BoxDailySquare.objects.get(user=user)
        except:
            box_daily_square = None
        if box_daily_square:
            context['box'] = box_daily_square
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

        if concept.concept_type == ConceptType.SIMPLE:
            movement = MovementPartnerHandler.create_simple(
                box_partner,
                concept,
                date,
                movement_type,
                value,
                detail,
                request.user,
                ip,
            )
        elif concept.concept_type == ConceptType.DOUBLE:
            movement = MovementPartnerHandler.create_double(
                partner,
                concept,
                date,
                movement_type,
                value,
                detail,
                request.user,
                ip,
            )
        elif concept.concept_type == ConceptType.SIMPLEDOUBLE:
            movement = MovementPartnerHandler.create_simple_double_movement(
                box_partner,
                concept,
                date,
                movement_type,
                value,
                detail,
                request.user,
                ip,
            )
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:partner_box', kwargs={'pk': request.POST['partner_id']}))


class CreateDailySquareMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.POST['user_id'])
        box_daily_square = BoxDailySquare.objects.get(user=user)
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

        movement = MovementDailySquare(
            box_daily_square=box_daily_square,
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
        return HttpResponseRedirect(reverse('webclient:daily_square_box', kwargs={'pk': request.POST['user_id']}))
