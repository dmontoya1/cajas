from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from units.admin import UnitInline
from cajas.users.forms import UserChangeForm, UserCreationForm
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.models.charges import Charge
from cajas.users.models.auth_logs import AuthLogs

User = get_user_model()

class EmployeeAdminInline(admin.StackedInline):

    model = Employee
    # list_display = ['get_full_name', 'employee_type']
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    model = Employee
    list_display = ['get_full_name', 'salary_type', 'salary']
    search_fields = ['user__first_name', 'user__last_name', 'salary',]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    model = Partner
    list_display = ['get_full_name', 'code', 'office', 'direct_partner', 'is_daily_square']
    search_fields = ['user__first_name', 'user__last_name', 'code', 'office__number', 'office__country__abbr',]
    extra = 0
    inlines= [UnitInline, ]
    readonly_fields = ('code', 'consecutive')

    class Media:
        js = (
            'js/admin/partner_admin.js',
        )


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets + (("Datos personales", {"fields": ("document_type", 'document_id', 'is_abstract')}),)
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ["first_name"]
    inlines = [EmployeeAdminInline,]


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):

    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(AuthLogs)
class AuthLogsAdmin(admin.ModelAdmin):
    """
    """

    list_display = ['user', 'date', 'action', 'ip' ]
    search_fields = ['user__first_name', 'user__last_name', 'date', 'action', 'ip' ]
