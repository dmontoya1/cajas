
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from boxes.views.box_daily_square.box_daily_square_handler import BoxDailySquareHandler
from cajas.users.models.partner import Partner
from cajas.users.services.user_service import UserManager
from cajas.users.services.partner_service import partner_manager
from movement.services.partner_service import MovementPartnerManager
from office.models.office import Office

from .get_ip import get_ip

user_manager = UserManager()
movement_partner_manager = MovementPartnerManager()


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
        if request.POST.get('direct_partner', None):
            direct_partner = Partner.objects.get(pk=request.POST['direct_partner'])
        else:
            direct_partner = None
        try:
            request.POST['daily_square']
            daily_square = True
        except:
            daily_square = False
        initial_value = request.POST['initial_value']
        office = Office.objects.get(pk=request.POST['office'])
        data_user = {
            'email': email,
            'username': email,
            'first_name': first_name,
            'last_name': last_name,
            'document_type': document_type,
            'document_id': document_id,
            'is_daily_square': daily_square
        }
        user = user_manager.create_user(data_user)
        data_partner = {
            'user': user,
            'office': office,
            'partner_type': partner_type,
            'direct_partner': direct_partner,
        }
        partner = partner_manager.create_partner(data_partner)
        if daily_square:
            box_daily_square = BoxDailySquareHandler.box_daily_square_create(user, office)
        if int(initial_value) > 0:
            ip = get_ip(request)
            data = {
                'partner': partner,
                'value': initial_value,
                'responsible': request.user,
                'ip': ip,
            }
            movement = movement_partner_manager.create_partner_movements(data)
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el socio exitosamente')
        return HttpResponseRedirect(reverse('webclient:partners_list', kwargs={'slug': office.slug}))
