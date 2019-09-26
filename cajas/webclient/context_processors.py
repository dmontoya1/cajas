
import logging

from django.db import connection
from django.db.models import Q

from tenant_schemas.utils import tenant_context

from cajas.api.models import APIKey
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry
from cajas.tenant.models import Platform
from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.models.user import User

logger = logging.getLogger(__name__)


def webclient_processor(request):
    schema_name = connection.schema_name
    tenant = Platform.objects.get(schema_name=schema_name)
    print("Contexto: ", schema_name)
    print("Contexto", tenant)

    with tenant_context(tenant):
        try:
            employee = Employee.objects.get(charge__name='Presidente')
            president = employee.user
        except:
            president = None
        try:
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
                    (Q(office__pk=request.session['office']) | Q(user=president)), Q(is_active=True)
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

            all_users = User.objects.all().exclude(email='super@admin.com')
            all_offices = OfficeCountry.objects.all()
            all_partners = Partner.objects.select_related('user', 'office', 'buyer_unit_partner').filter(is_active=True)
            concepts = Concept.objects.filter(is_active=True)
            api_key, created = APIKey.objects.get_or_create(name='webclient')
            context = {
                'API_KEY': api_key.key,
                'concepts': concepts,
                'partners': partners,
                'all_partners': all_partners,
                'all_users': all_users,
                'all_offices': all_offices,
                'office_employees': employees,
                'session_employee': session_employee,
                'is_admin_charge': is_admin_charge,
                'request_user': request.user,
                'is_secretary': is_secretary,
                'is_admin_senior': is_admin_senior,
                'president': president.get_full_name()
            }
            print("Contextoooo: ", context['president'])
        except Exception as e:
            print(e)
            logger.exception("Exception en Context Processor", e)
            context = {}
        return context
