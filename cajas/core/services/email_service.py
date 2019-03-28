from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import reverse


class EmailManager(object):
    template = 'email/email.html'
    email_to = settings.ADMIN_EMAIL

    def send_email(self, url, ctx, subject):
        body = get_template(self.template).render(ctx)
        message = EmailMessage(subject, body, settings.EMAIL_USER,
                               [self.email_to])
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
        self.send_email(url, ctx, subject)

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
        self.send_email(url, ctx, subject)
