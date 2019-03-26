from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models.movement_country import MovementCountry
from .models.movement_daily_square import MovementDailySquare
from .models.movement_don_juan import MovementDonJuan
from .models.movement_office import MovementOffice
from .models.movement_partner import MovementPartner
from .models.movement_provisioning import MovementProvisioning
from .models.movement_request import MovementRequest


class MovementCountryInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un país
    """

    model = MovementCountry
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementDailySquareInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un cuadre diario
    """

    model = MovementDailySquare
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementDonJuanInline(admin.TabularInline):
    """Inline para los movimientos de la caja de Don Juan
    """

    model = MovementDonJuan
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementOfficeInline(admin.TabularInline):
    """Inline para los movimientos de la caja de una oficina
    """

    model = MovementOffice
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementPartnerInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un socio
    """

    model = MovementPartner
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementProvisioningInline(admin.TabularInline):
    """Inline para los movimientos de la caja de una oficina
    """

    model = MovementProvisioning
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


@admin.register(MovementRequest)
class MovementRequestAdmin(admin.ModelAdmin):

    list_display = ('box_partner', 'date', 'concept', )
    readonly_fields = ('box_partner', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip')
    exclude = ('balance', )
