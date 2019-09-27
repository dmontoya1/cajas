from django.contrib import admin
from django.utils.safestring import mark_safe

from cajas.movement.admin import (
    MovementDonJuanUSDInline,
    MovementDonJuanInline,
    MovementOfficeInline,
    MovementProvisioningInline
)

from .models.box_colombia import BoxColombia
from .models.box_daily_square import BoxDailySquare
from .models.box_don_juan import BoxDonJuan
from .models.box_don_juan_usd import BoxDonJuanUSD
from .models.box_office import BoxOffice
from .models.box_partner import BoxPartner
from .models.box_provisioning import BoxProvisioning


@admin.register(BoxColombia)
class BoxColombiaAdmin(admin.ModelAdmin):
    """Administrador de las cajas colombia
        Se agrega INLINE con los movimientos
    """

    list_display = ('office', 'name', 'balance', 'is_active', 'get_edit_link')
    readonly_fields = ["get_edit_link", ]
    search_fields = ('office__name',)
    exclude = ('last_movement_id',)

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = '/admin/movement/movementboxcolombia/?box_office__id__exact={}'.format(obj.pk)
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Ver movimientos de la caja",
            ))
        return "Guarde y continúe editando para poder ver los movimientos"

    get_edit_link.short_description = "Movimientos"
    get_edit_link.allow_tags = True


@admin.register(BoxDailySquare)
class BoxDailySquareAdmin(admin.ModelAdmin):
    """Administrador de las cajas de un cuadre diario
        Se agrega INLINE con los movimientos
    """

    list_display = ('user', 'office', 'balance', 'is_active', 'get_edit_link')
    readonly_fields = ["get_edit_link", ]
    search_fields = ('user__first_name', 'user__last_name', 'user__document_id')
    exclude = ('last_movement_id', )

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = '/admin/movement/movementdailysquare/?box_daily_square__id__exact={}'.format(obj.pk)
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Ver movimientos de la caja",
            ))
        return "Guarde y continúe editando para poder ver los movimientos"

    get_edit_link.short_description = "Movimientos"
    get_edit_link.allow_tags = True


@admin.register(BoxDonJuan)
class BoxDonJuanAdmin(admin.ModelAdmin):
    """Administrador de las cajas del Presidente por oficina
        Se agrega INLINE con los movimientos
    """

    list_display = ('office', 'balance', 'is_active', 'get_edit_link')
    readonly_fields = ["get_edit_link", ]
    search_fields = ('office__country__abbr', )
    exclude = ('last_movement_id', )

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = '/admin/movement/movementdonjuan/?box_don_juan__id__exact={}'.format(obj.pk)
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Ver movimientos de la caja",
            ))
        return "Guarde y continúe editando para poder ver los movimientos"

    get_edit_link.short_description = "Movimientos"
    get_edit_link.allow_tags = True


@admin.register(BoxDonJuanUSD)
class BoxDonJuanUSDAdmin(admin.ModelAdmin):
    """Administrador de las cajas del presidente por oficina
        Se agrega INLINE con los movimientos
    """

    list_display = ('office', 'balance', 'is_active')
    inlines = [MovementDonJuanUSDInline, ]
    search_fields = ('office__country__abbr', 'office__number', )
    exclude = ('last_movement_id', )


@admin.register(BoxOffice)
class BoxOfficeAdmin(admin.ModelAdmin):
    """Administrador de las cajas de una oficina
        Se agrega INLINE con los movimientos
    """

    list_display = ('office', 'balance', 'is_active')
    inlines = [MovementOfficeInline, ]
    search_fields = ('office__name', )
    exclude = ('last_movement_id', )


@admin.register(BoxPartner)
class BoxPartnerAdmin(admin.ModelAdmin):
    """Administrador de las cajas de un socio
        Se agrega INLINE con los movimientos
    """

    list_display = ('partner', 'balance', 'box_status', 'get_edit_link')
    readonly_fields = ["get_edit_link", ]
    list_filter = ('partner__office', 'box_status')
    search_fields = ('partner__user__first_name', 'partner__user__last_name', 'partner__code',
                     'partner__user__document_id')
    exclude = ('last_movement_id', )

    def get_edit_link(self, obj=None):
        if obj.pk:
            url = '/admin/movement/movementpartner/?box_partner__partner__id__exact={}'.format(obj.pk)
            return mark_safe("""<a href="{url}" target="_blank">{text}</a>""".format(
                url=url,
                text="Ver movimientos de la caja",
            ))
        return "Guarde y continúe editando para poder ver los movimientos"

    get_edit_link.short_description = "Movimientos"
    get_edit_link.allow_tags = True


@admin.register(BoxProvisioning)
class BoxProvisioningAdmin(admin.ModelAdmin):
    """Administrador de las cajas de una oficina
        Se agrega INLINE con los movimientos
    """

    list_display = ('office', 'balance', 'is_active')
    inlines = [MovementProvisioningInline, ]
    search_fields = ('office__name', )
    exclude = ('last_movement_id', )
