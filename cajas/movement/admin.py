from django.contrib import admin

from .models.movement_country import MovementCountry
from .models.movement_daily_square import MovementDailySquare
from .models.movement_office import MovementOffice
from .models.movement_partner import MovementPartner


class MovementCountryInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un país
    """

    model = MovementCountry
    extra = 0


class MovementDailySquareInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un cuadre diario
    """

    model = MovementDailySquare
    extra = 0


class MovementOfficeInline(admin.TabularInline):
    """Inline para los movimientos de la caja de una oficina
    """

    model = MovementOffice
    extra = 0


class MovementPartnerInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un socio
    """

    model = MovementPartner
    extra = 0

