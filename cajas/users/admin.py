from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from cajas.users.forms import UserChangeForm, UserCreationForm
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets + (("Datos personales", {"fields": ("document_type", 'document_id', 'is_abstract')}),)
    list_display = ["username", "first_name", "last_name", "is_superuser"]
    search_fields = ["first_name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    model = Employee
    list_display = ['get_full_name', 'employee_type']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):

    model = Partner
    list_display = ['get_full_name', 'code', 'direct_partner']
