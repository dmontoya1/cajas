from allauth.account.signals import user_logged_in, user_logged_out

from django.db import connection
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from tenant_schemas.utils import tenant_context

from cajas.boxes.models.box_partner import BoxPartner
from cajas.core.services.email_service import EmailManager
from cajas.users.models.auth_logs import AuthLogs
from cajas.users.models.partner import Partner
from cajas.users.models.employee import Employee
from cajas.tenant.models import Platform
from cajas.webclient.views.get_ip import get_ip
email_manager = EmailManager()


@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    schema_name = connection.schema_name
    tenant1 = Platform.objects.get(schema_name=schema_name)
    with tenant_context(tenant1):
        ip = get_ip(request)

        log = AuthLogs(
            ip=ip,
            user=user,
            action=AuthLogs.LOGIN
        )
        log.save()


@receiver(user_logged_out)
def after_user_logged_out(sender, request, user, **kwargs):
    schema_name = connection.schema_name
    tenant1 = Platform.objects.get(schema_name=schema_name)
    with tenant_context(tenant1):
        ip = get_ip(request)

        log = AuthLogs(
            ip=ip,
            user=user,
            action=AuthLogs.LOGOUT
        )
        log.save()


@receiver(post_save, sender=Partner)
def create_partner_box(sender, **kwargs):
    schema_name = connection.schema_name
    tenant1 = Platform.objects.get(schema_name=schema_name)
    with tenant_context(tenant1):
        if kwargs.get('created'):
            instance = kwargs.get('instance')
            box = BoxPartner(
                partner=instance,
            )
            box.save()


@receiver(pre_save, sender=Employee)
def send_mail_when_salary_value_changes(sender, instance, **kwargs):
    schema_name = connection.schema_name
    tenant1 = Platform.objects.get(schema_name=schema_name)
    with tenant_context(tenant1):
        try:
            old = Employee.objects.get(pk=instance.pk)
        except:
            old = None
        if old is not None:
            if float(old.salary) != float(instance.salary):
                email_manager.send_employee_salary_change_notification(instance)
