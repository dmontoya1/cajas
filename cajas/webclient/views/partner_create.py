
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from cajas.boxes.services.box_daily_square_manager import BoxDailySquareManager
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.services.user_service import UserManager
from cajas.users.services.partner_service import PartnerManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.movement.services.daily_square_service import MovementDailySquareManager
from cajas.office.models.officeCountry import OfficeCountry
from cajas.webclient.views.utils import get_object_or_none

from .get_ip import get_ip

box_daily_square_manager = BoxDailySquareManager()
daily_square_manager = MovementDailySquareManager()
movement_partner_manager = MovementPartnerManager()
partner_manager = PartnerManager()
user_manager = UserManager()


class PartnerCreate(LoginRequiredMixin, View):
    """
    """

    def post(self, request, *args, **kwargs):
        office = OfficeCountry.objects.get(pk=request.POST['office'])
        admin_senior = get_object_or_none(Employee, office=office.office, charge__name='Administrador Senior')
        if not admin_senior:
            messages.add_message(
                request,
                messages.ERROR,
                'No hay ningún Administrador Senior en la oficina. Para continuar Agrega uno.'
            )
            return HttpResponseRedirect(reverse('webclient:partners_list', kwargs={'slug': office.slug}))
        if not admin_senior.user.is_daily_square:
            messages.add_message(
                request,
                messages.ERROR,
                'El administrador Senior no tiene un cuadre diario asociado'
            )
            return HttpResponseRedirect(reverse('webclient:partners_list', kwargs={'slug': office.slug}))
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

        if partner_type == 'INDIR' and not direct_partner:
            messages.add_message(
                request,
                messages.ERROR,
                'Has seleccionado socio indirecto pero no seleccionaste el socio directo. Ingresa el socio directo.'
            )
            return HttpResponseRedirect(reverse('webclient:partners_list', kwargs={'slug': office.slug}))
        if 'daily_square' in request.POST:
            request.POST['daily_square']
            daily_square = "true"
        else:
            daily_square = "false"
        initial_value = request.POST['initial_value']

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
            data = {
                'user': user,
                'office': office
            }
            box_daily_square = box_daily_square_manager.create_box(data)
        if int(initial_value) > 0:
            ip = get_ip(request)
            data = {
                'partner': partner,
                'value': initial_value,
                'responsible': request.user,
                'ip': ip,
            }
            movement = movement_partner_manager.create_partner_movements(data)
            data['box'] = admin_senior.user.related_daily_box.filter(office=office).first()
            movement1 = daily_square_manager.create_new_partner_movement(data)
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el socio exitosamente')
        return HttpResponseRedirect(reverse('webclient:partners_list', kwargs={'slug': office.slug}))
