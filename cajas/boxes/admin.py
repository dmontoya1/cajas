from django.contrib import admin


from movement.admin import MovementCountryInline, MovementDailySquareInline, MovementOfficeInline,  MovementPartnerInline

from .models.box_country import BoxCountry
from .models.box_daily_square import BoxDailySquare
from .models.box_office import BoxOffice
from .models.box_partner import BoxPartner


@admin.register(BoxCountry)
class BoxCountryAdmin(admin.ModelAdmin):
    """Administrador de las cajas de un país
        Se agrega INLINE con los movimientos
    """

    list_display = ('country', 'balance', 'currency', 'is_active')
    inlines = [MovementCountryInline, ]
    search_fields = ('country__name', 'currency__name', 'currency__abbr' )
    exclude = ('last_movement_id', )


@admin.register(BoxDailySquare)
class BoxDailySquareAdmin(admin.ModelAdmin):
    """Administrador de las cajas de un cuadre diario
        Se agrega INLINE con los movimientos
    """

    list_display = ('user', 'balance', 'is_active')
    inlines = [MovementDailySquareInline, ]
    search_fields = ('user__first_name', 'user__last_name', 'user__document_id' )
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

    list_display = ('partner', 'balance', 'is_active')
    inlines = [MovementPartnerInline, ]
    search_fields = ('partner__user__first_name', 'partner__user__last_name', 'partner__code', 'partner__user__document_id' )
    exclude = ('last_movement_id', )

