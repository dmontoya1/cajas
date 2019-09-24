from django.contrib import admin

from .models.office import Office
from .models.officeItems import OfficeItems
from .models.officeCommitments import OfficeCommitments
from .models.officeCountry import OfficeCountry
from .models.supervisorCalendar import SupervisorCalendar
from .models.notifications import Notifications


@admin.register(OfficeItems)
class OfficeItemsAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('office', 'name', 'price', 'brand')
    list_filter = ('office', 'office__country', 'office__office')


class OfficeCommitmentsAdmin(admin.StackedInline):
    """
    """

    model = OfficeCommitments
    extra = 1


@admin.register(OfficeCountry)
class OfficeCountryAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('__str__', )
    search_fields = ('number', )


class OfficeCountryInline(admin.StackedInline):
    """
    """

    model = OfficeCountry
    extra = 0
    readonly_fields = ('consecutive',)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('__str__', )
    search_fields = ('number', )
    inlines = [OfficeCountryInline, OfficeCommitmentsAdmin]


@admin.register(SupervisorCalendar)
class SupervisorCalendarAdmin(admin.ModelAdmin):
    """
    """

    model = SupervisorCalendar
    extra = 0


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    """
    """

    model = Notifications
    extra = 0
