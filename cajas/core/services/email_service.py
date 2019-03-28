from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import reverse


class EmailManager(object):
    template = 'email/email.html'
    email_to = settings.ADMIN_EMAIL

    def send_email(self, url, ctx, subject, email_to):
        body = get_template(self.template).render(ctx)
        message = EmailMessage(subject, body, settings.EMAIL_USER,
                               [email_to])
        message.content_subtype = 'html'
        message.send()

    def send_stop_email(self, request):

        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:movement_required'))
        ctx = {
            "title": "Nueva solicitud de aprobación de movimiento",
            "content": "Ha llegado una nueva solicitud de aprobación de movimiento por paso del tope permitido. "
                       "Entra al siguiente link para que lo revises"
            ,
            "url": url,
            "action": "Ver solicitud"
        }
        subject = "Nueva solicitud de aprobación de movimiento"
        self.send_email(url, ctx, subject, self.email_to)

    def send_withdraw_email(self, request):
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:movement_withdraw_required'))
        ctx = {
            "title": "Nueva solicitud de retiro de socio",
            "content": "Ha llegado una nueva solicitud de aprobación de retiro de socio. "
                       "Entra al siguiente link para que lo revises"
            ,
            "url": url,
            "action": "Ver solicitud"
        }
        subject = "Nueva solicitud de retiro de socio"
        self.send_email(url, ctx, subject, self.email_to)

    def send_withdraw_accept_email(self, request, email_to):
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:home'))
        ctx = {
            "title": "Solicitud de retiro aprobada",
            "content": "Se ha aprobado la solicitud de retiro de socio. Se ha creado el movimiento en tu caja. "
                       "Entra a la plataforma para que lo revises"
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Nueva solicitud de retiro de socio"
        self.send_email(url, ctx, subject, email_to)
