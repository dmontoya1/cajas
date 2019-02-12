
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from units.models.units import Unit
from units.models.unitItems import UnitItems


class UnitItemsAdmin(admin.StackedInline):
    """
    """

    model = UnitItems
    extra = 1


class UnitInline(admin.StackedInline):
    model = Unit
    extra = 0
    fields = ["name", "partner", "collector", "supervisor", "get_edit_link", ]
    readonly_fields = ["get_edit_link",]

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Editar esta %s separadamente" % obj._meta.verbose_name,
            ))
        return _("Guarde y continúe editando para poder ver el link de edición")
    get_edit_link.short_description = "Editar Unidad"
    get_edit_link.allow_tags = True


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('name', 'partner', 'collector', 'supervisor')
    search_fields = ('name', 'partner__first_name', 'partner__partner__code')
    inlines = [UnitItemsAdmin, ]
    save_on_top = True
