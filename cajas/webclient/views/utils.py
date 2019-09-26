
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404

from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee


def _get_queryset(klass):
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def get_object_or_none(klass, *args, **kwargs):
    """
    Use get() to return an object, or return None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """

    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_none() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def is_secretary(user, office):
    secretary = Charge.objects.get(name="Secretaria")
    try:
        employee = Employee.objects.get(
            Q(user=user),
            (Q(office_country=office) | Q(office=office.office))
        )
        return employee.charge == secretary
    except Employee.DoesNotExist:
        return False


def is_admin_senior(user, office):
    admin = Charge.objects.get(name="Administrador Senior")
    try:
        employee = Employee.objects.get(
                Q(user=user),
                Q(office_country=office) |
                Q(office=office.office)
            )
        return employee.charge == admin
    except Employee.DoesNotExist:
        return False


def get_president_user():
    charge = get_object_or_404(Charge, name="Presidente")
    try:
        employee = Employee.objects.get(charge=charge)
        return employee.user
    except:
        return None
