

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from cajas.core.services.email_service import EmailManager


class Landing(TemplateView):
    """
    """

    template_name = 'webclient/landing.html'

    def post(self, request):
        data = request.POST
        send_email = EmailManager()
        data_send = {
            'name': data['et_pb_contact_name_0'],
            'email': data['et_pb_contact_email_0'],
            'phone': data['et_pb_contact_telefono_0'],
            'message': data['et_pb_contact_message_0']
        }
        send_email.send_landing_email(data_send)
        messages.add_message(request, messages.SUCCESS, 'Se ha enviado el mensaje correctamente')
        return HttpResponseRedirect(reverse('webclient:landing'))
