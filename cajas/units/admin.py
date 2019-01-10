
from django.contrib import admin

from units.models.units import Unit
from units.models.unitItems import UnitItems


class UnitItemsAdmin(admin.StackedInline):
    """
    """

    model = UnitItems
    extra = 1


@admin.register(Unit)
class UnirAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('name', 'partner', 'collector', 'supervisor')
    search_fields = ('name', 'partner__first_name', 'partner__partner__code')
    inlines = [UnitItemsAdmin, ]
