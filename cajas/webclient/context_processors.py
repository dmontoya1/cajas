from django.conf import settings
from django.db.models import Q

from cajas.users.models.partner import Partner
from cajas.users.models.employee import Employee
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry


def webclient_processor(request):
    if 'office' in request.session:
        office_country = OfficeCountry.objects.get(pk=request.session['office'])
        partners = Partner.objects.filter(
            (Q(office__pk=request.session['office']) |
             Q(code='DONJUAN'))
            & Q(is_active=True)
        )
        employees = Employee.objects.filter(
            Q(office_country=office_country) or
            Q(office=office_country.office) and
            Q(is_active=True))
    else:
        partners = None
        employees = None
    all_partners = Partner.objects.filter(is_active=True)
    concepts = Concept.objects.filter(is_active=True)
    context = {
        'API_KEY': settings.API_KEY,
        'concepts': concepts,
        'partners': partners,
        'all_partners': all_partners,
        'office_employees': employees
    }

    return context
