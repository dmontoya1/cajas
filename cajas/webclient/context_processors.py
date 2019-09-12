from django.conf import settings
from django.db.models import Q

from cajas.users.models.partner import Partner
from cajas.users.models.employee import Employee
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.charges import Charge


def webclient_processor(request):

    secretary = Charge.objects.get(name="Secretaria")
    admin_senior = Charge.objects.get(name="Administrador Senior")
    is_secretary = None
    is_admin_senior = None
    is_admin_charge = None
    partners = None
    employees = None
    session_employee = None
    if 'office' in request.session:
        office_country = OfficeCountry.objects.select_related('office', 'country', 'box').get(
            pk=request.session['office']
        )
        partners = Partner.objects.select_related('user', 'office', 'buyer_unit_partner').filter(
            (Q(office__pk=request.session['office']) |
             Q(code='DONJUAN')), Q(is_active=True)
        )
        employees = Employee.objects.select_related('user', 'charge', 'dailysquareunits').filter(
            Q(office_country=office_country) | Q(office=office_country.office)
        )
        if not request.user.is_superuser:
            try:
                session_employee = Employee.objects.get(
                    Q(user=request.user), (Q(office_country=office_country) | Q(office=office_country.office))
                )
            except Exception as e:
                print(e)
                session_employee = None
    elif not request.user.is_anonymous:
        session_employee = Employee.objects.filter(
            user=request.user
        ).first()
    if not request.user.is_superuser:
        if session_employee:
            if session_employee.charge == secretary:
                is_secretary = True
                is_admin_senior = False
            elif session_employee.charge == admin_senior:
                is_secretary = False
                is_admin_senior = True
            if session_employee.charge == secretary or session_employee.charge == admin_senior:
                is_admin_charge = True
            else:
                is_admin_senior = False

    all_partners = Partner.objects.select_related('user', 'office', 'buyer_unit_partner').filter(is_active=True)
    concepts = Concept.objects.filter(is_active=True)
    context = {
        'API_KEY': settings.API_KEY,
        'concepts': concepts,
        'partners': partners,
        'all_partners': all_partners,
        'office_employees': employees,
        'session_employee': session_employee,
        'is_admin_charge': is_admin_charge,
        'request_user': request.user,
        'is_secretary': is_secretary,
        'is_admin_senior': is_admin_senior
    }

    return context
