from django.contrib import admin

from office.models.office import Office
from office.models.officeItems import OfficeItems
from office.models.officeCommitments import OfficeCommitments
from office.models.supervisorCalendar import SupervisorCalendar


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

    list_display = ('country', 'number', )
    search_fields = ('number', 'country__name')
    readonly_fields = ('slug', 'consecutive')
    inlines = [OfficeItemsAdmin, OfficeCommitmentsAdmin]


@admin.register(SupervisorCalendar)
class SupervisorCalendarAdmin(admin.ModelAdmin):
    """
    """

    model = SupervisorCalendar
    extra = 0
