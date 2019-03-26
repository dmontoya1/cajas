from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import reverse


class EmailManager(object):
    template = 'email/email.html'
    email_to = settings.ADMIN_EMAIL

    def sendStopEmail(self, request):
        """Función para enviar mensajes en la plataforma

        Esta función se utiliza para enviar mensajes en la plataforma, recibe como parámetros
        un contexto, el email hacia quien va dirigido, Asunto y el template base
        del correo
        """
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:movement_required'))
        ctx = {
            "title": "Nueva solicitud de aprobación de movimiento",
            "content": "Ha llegado una nueva solicitud de aprobación de movimiento por paso del tope permitido. "
                       "Entra al siguiente link para que lo revises"
            ,
            "url": url,
            "action": "Ver solicitud"
        }
        body = get_template(self.template).render(ctx)
        message = EmailMessage("Nueva solicitud de aprobación de movimiento", body, settings.EMAIL_USER, [self.email_to])
        message.content_subtype = 'html'
        message.send()
