
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View

from boxes.models.box_office import BoxOffice
from concepts.models.concepts import Concept
from movement.models.movement_office import MovementOffice
from office.models.office import Office


class Home(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        concepts = Concept.objects.filter(is_active=True)
        try:
            office = Office.objects.get(secretary=self.request.user.employee)
        except:
            office = None
        if office:
            context['office'] = office
        context['concepts'] = concepts
        return context


class CreateOfficeMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        print (request.POST)
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
