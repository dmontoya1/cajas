from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _

from cajas.units.admin import UnitInline

from .forms import UserChangeForm, UserCreationForm
from .models import Employee, Partner, Charge, AuthLogs, Group, GroupEmployee, DailySquareUnits

User = get_user_model()


class DailySquareUnitsInline(admin.StackedInline):

    model = DailySquareUnits
    extra = 1


class EmployeeAdminInline(admin.StackedInline):

    model = Employee
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    model = Employee
    list_display = ['get_full_name', 'charge', 'salary_type', 'salary', 'get_office_country']
    search_fields = ['user__first_name', 'user__last_name', 'salary', ]
    list_filter = ['charge', ]
    inlines = [DailySquareUnitsInline, ]

    def get_office_country(self, obj):
        return "\n -".join([str(o) for o in obj.office_country.all()])

    class Media:
        js = (
            'js/admin/employee_admin.js',
        )

    get_office_country.short_description = 'Oficina País'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    model = Partner
    list_display = ['get_full_name', 'code', 'partner_type', 'get_direct_partner',]
    search_fields = ['user__first_name', 'user__last_name', 'code', ]
    extra = 0
    list_filter = ['office', 'office__office', 'office__country']
    inlines = [UnitInline, ]
    readonly_fields = ('consecutive', )
    fieldsets = (("Datos Socio",
        {"fields": ("user", 'office', 'code', 'partner_type', 'direct_partner', 'consecutive', 'is_active',
                    'buyer_unit_partner')}),)

    def get_direct_partner(self, obj):
        if obj.direct_partner:
            return obj.direct_partner.get_full_name()
        return 'Presidente'

    get_direct_partner.short_description = 'Socio Directo'


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets + (("Datos personales",
        {"fields": ("document_type", 'document_id', 'is_abstract', 'is_daily_square')}),)
    list_display = ["email", "first_name", "last_name", "is_daily_square"]
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ["first_name", 'last_name', 'document_id', 'email', 'username']
    inlines = [EmployeeAdminInline, ]


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):

    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(AuthLogs)
class AuthLogsAdmin(admin.ModelAdmin):
    """
    """

    list_display = ['user', 'date', 'action', 'ip']
    search_fields = ['user__first_name', 'user__last_name', 'date', 'action', 'ip']


class GroupEmployeeInline(admin.StackedInline):
    """
    """

    model = GroupEmployee
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "supervisor":
            kwargs["queryset"] = Employee.objects.filter(charge__name="Supervisor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    """

    list_display = ['admin', ]
    inlines = [GroupEmployeeInline, ]
