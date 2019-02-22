
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from boxes.models.box_partner import BoxPartner
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from concepts.models.concepts import Concept, ConceptType
from movement.views.movement_partner.movement_partner_handler import MovementPartnerHandler

from .get_ip import get_ip


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

        ip = get_ip(request)

        if concept.concept_type == ConceptType.SIMPLE:
            data = {
                'box': box_partner,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
            }
            movement = MovementPartnerHandler.create_simple(data)
        elif concept.concept_type == ConceptType.DOUBLE:
            data = {
                'partner': partner,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
            }
            movement = MovementPartnerHandler.create_double(data)
        elif concept.concept_type == ConceptType.SIMPLEDOUBLE:
            data = {
                'partner': partner,
                'concept': concept,
                'date': date,
                'movement_type': movement_type,
                'value': value,
                'detail': detail,
                'responsible': request.user,
                'ip': ip,
            }
            movement = MovementPartnerHandler.create_simple_double_movement(data)
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:partner_box', kwargs={'pk': request.POST['partner_id']}))
