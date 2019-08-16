from django.db.models import Q

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import reverse

from cajas.concepts.models.stops import Stop
from cajas.users.models.employee import Employee


class EmailManager(object):
    template = 'email/email.html'
    email_to = settings.ADMIN_EMAIL

    def send_email(self, ctx, subject, email_to):
        body = get_template(self.template).render(ctx)
        message = EmailMessage(subject, body, settings.EMAIL_USER,
                               [email_to])
        message.content_subtype = 'html'
        try:
            message.send()
        except Exception as e:
            print(e)

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
        self.send_email(ctx, subject, self.email_to)

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
        self.send_email(ctx, subject, self.email_to)

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
        self.send_email(ctx, subject, email_to)

    def send_denied_between_office_movement_email(self, request, movement, email_to):
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:home'))
        ctx = {
            "title": "Movimiento entre oficinas rechazado",
            "content": "Se ha rechazado el movimiento por concepto de {}: {}, del dia {}. \
                       Entra a la plataforma para que lo revises".format(
                movement.concept,
                movement.detail,
                movement.date
            ),
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Movimiento entre oficinas rechazado"
        self.send_email(ctx, subject, email_to)

    def send_cd_transfer_email(self, request, dq_from, value, email_to):
        url = 'http://{}{}'.format(request.get_host(), reverse('webclient:home'))
        ctx = {
            "title": "Te han hecho un traslado de efeectivo",
            "content": "El cuadre diario {} te ha hecho un traslado de efectivo por valor de ${}.".format(
                dq_from,
                value,
            ),
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Te han hecho un traslado de efeectivo"
        self.send_email(ctx, subject, email_to)

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
        self.send_email(ctx, subject, email_to)

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
        self.send_email(ctx, subject, email_to)

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
        self.send_email(ctx, subject, email_to)

    def send_employee_salary_change_notification(self, employee):
        domain = Site.objects.get_current().domain
        url = 'http://{}{}'.format(domain, reverse('webclient:home'))
        ctx = {
            "title": "Cambio de Salario",
            "content": "El salario del empleado {} ha cambiado".format(employee)
            ,
            "url": url,
            "action": "Ir a la plataforma"
        }
        subject = "Notificación de cambio de salario"
        self.send_email(ctx, subject, self.email_to)

    def send_informative_top_notification(self, user, concept):
        domain = Site.objects.get_current().domain
        try:
            charge = user.employee.get().charge
        except:
            charge = None
        stops = Stop.objects.filter(
            Q(concept=concept) &
            Q(is_informative=True) &
            (Q(charge=charge) | Q(user=user))
        )
        url = 'http://{}{}'.format(domain, reverse('webclient:home'))
        for stop in stops:
            for report_user in stop.report_users.all():
                ctx = {
                    "title": "Tope informativo",
                    "content": "{} ha superado el tope informativo".format(user)
                    ,
                    "url": url,
                    "action": "Ir a la plataforma"
                }
                subject = "Tope informativo"
                self.send_email(ctx, subject, report_user.email)

            employees = Employee.objects.filter(charge=stop.report_by_charge)
            for e in employees:
                ctx = {
                    "title": "Tope informativo",
                    "content": "{} ha superado el tope informativo".format(user)
                    ,
                    "url": url,
                    "action": "Ir a la plataforma"
                }
                subject = "Tope informativo"
                self.send_email(ctx, subject, e.user.email)
