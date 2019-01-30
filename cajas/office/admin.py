from django.contrib import admin

from office.models.office import Office
from office.models.officeItems import OfficeItems
from office.models.officeCommitments import OfficeCommitments

from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee


class OfficeItemsAdmin(admin.StackedInline):
    """
    """

    model = OfficeItems
    extra = 0


class OfficeCommitmentsAdmin(admin.StackedInline):
    """
    """

    model = OfficeCommitments
    extra = 1


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('name', 'country', 'secretary')
    search_fields = ('name', 'country__name')
    inlines = [OfficeItemsAdmin, OfficeCommitmentsAdmin]


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "admin_senior":
            charge = Charge.objects.filter(name__contains="Administrador Senior").first()
            kwargs["queryset"] = Employee.objects.filter(charge=charge).order_by('pk')
        if db_field.name == "admin_junior":
            charge = Charge.objects.filter(name__contains="Administrador Junior").first()
            kwargs["queryset"] = Employee.objects.filter(charge=charge).order_by('pk')
        if db_field.name == "secretary":
            charge = Charge.objects.filter(name__contains="Secretaria").first()
            kwargs["queryset"] = Employee.objects.filter(charge=charge).order_by('pk')
        return super(OfficeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
