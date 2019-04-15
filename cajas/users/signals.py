from allauth.account.signals import user_logged_in, user_logged_out

from django.db.models.signals import post_save
from django.dispatch import receiver

from boxes.models.box_daily_square import BoxDailySquare
from boxes.models.box_partner import BoxPartner
from cajas.users.models.auth_logs import AuthLogs
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.models.employee import Employee
from cajas.users.models.group import Group

from webclient.views.get_ip import get_ip


@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    ip = get_ip(request)

    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGIN
    )
    log.save()


@receiver(user_logged_out)
def after_user_logged_out(sender, request, user, **kwargs):
    ip = get_ip(request)

    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGOUT
    )
    log.save()


@receiver(post_save, sender=Partner)
def create_partner_box(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        box = BoxPartner(
            partner=instance,
        )
        box.save()


@receiver(post_save, sender=Employee)
def create_employee_admin_group(sender, instance, **kwargs):
    if kwargs.get('created'):
        if instance.charge == "Administrador de Grupo":
            Group.objects.create(admin=instance)
