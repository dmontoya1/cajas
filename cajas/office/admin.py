from django.contrib import admin

from .models.office import Office
from .models.officeItems import OfficeItems
from .models.officeCommitments import OfficeCommitments
from .models.officeCountry import OfficeCountry
from .models.supervisorCalendar import SupervisorCalendar


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


class OfficeCountryInline(admin.StackedInline):
    """
    """

    model = OfficeCountry
    extra = 0
    readonly_fields = ('slug', 'consecutive',)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('__str__', )
    search_fields = ('number', )
    inlines = [OfficeCountryInline, OfficeItemsAdmin, OfficeCommitmentsAdmin]


@admin.register(SupervisorCalendar)
class SupervisorCalendarAdmin(admin.ModelAdmin):
    """
    """

    model = SupervisorCalendar
    extra = 0
