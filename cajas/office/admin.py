from django.contrib import admin

from office.models.office import Office
from office.models.officeItems import OfficeItems
from office.models.officeCommitments import OfficeCommitments


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
