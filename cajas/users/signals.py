from allauth.account.signals import user_logged_in, user_logged_out

from django.dispatch import receiver

from cajas.users.models.auth_logs import AuthLogs

@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGIN
    )
    log.save()

@receiver(user_logged_out)
def after_user_logged_out(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGOUT
    )
    log.save()


