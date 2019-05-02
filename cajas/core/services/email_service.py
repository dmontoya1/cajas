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

    def send_office_mail(self, request, email_to):
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:home'))
        ctx = {
            "title": "Has recibido una transferencia de otra oficina",
            "content": "Has recibido una transferencia desde otra oficina. Para revisarlo ve a la caja de tu oficina"
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Has recibido una transferencia de otra oficina"
        self.send_email(url, ctx, subject, email_to)

    def send_close_box_mail(self, domain, email_to):
        url = 'http://{}{}'.format(domain, reverse('webclient:home'))
        ctx = {
            "title": "Notificación de cierre de cuadre diario",
            "content": "Aún no has cerrado la caja de cuadre diario, ingresa a la plataforma y revisa el estado de tu caja"
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Notificación de cierre de cuadre diario"
        self.send_email(url, ctx, subject, email_to)

    def send_payment_notification(self, domain, email_to):
        url = 'http://{}{}'.format(domain, reverse('webclient:home'))
        ctx = {
            "title": "Recordatorio de Pagos",
            "content": "Recuerda el pago de intereses, abonos y prestámos"
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Recodatorio de pagos"
        self.send_email(url, ctx, subject, email_to)

    def send_employee_salary_change_notification(self, employee, domain, email_to):
        url = 'http://{}{}'.format(domain, reverse('webclient:home'))
        ctx = {
            "title": "Cambio de Salario",
            "content": "El salario del empleado {} ha cambiado".format(employee)
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Notificación de cambio de salario"
        self.send_email(url, ctx, subject, email_to)
