from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from .models.user_place import UserPlace
from .models.chain_place import ChainPlace
from .models.chain import Chain


class ChainPlaceInline(admin.StackedInline):
    """
    """

    model = ChainPlace
    fields = ["pay_date", "get_edit_link", ]
    readonly_fields = ["get_edit_link", ]
    extra = 0

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Ver usuarios por puesto",
            ))
        return "Guarde y continúe editando para poder ver el link de edición"

    get_edit_link.short_description = "Editar puesto"
    get_edit_link.allow_tags = True


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):

    list_display = ('name', 'places', 'place_value', 'external_chain', )
    search_fields = ('name', 'places', )
    inlines = [ChainPlaceInline, ]


class UserPlaceStacked(admin.StackedInline):

    model = UserPlace
    extra = 0


@admin.register(ChainPlace)
class ChainPlaceAdmin(admin.ModelAdmin):

    list_display = ('chain', 'pay_date', )
    readonly_fields = ('chain', )
    inlines = [UserPlaceStacked, ]
