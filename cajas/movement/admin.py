from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models.movement_box_colombia import MovementBoxColombia
from .models.movement_daily_square import MovementDailySquare
from .models.movement_don_juan import MovementDonJuan
from .models.movement_don_juan_usd import MovementDonJuanUsd
from .models.movement_office import MovementOffice
from .models.movement_partner import MovementPartner
from .models.movement_provisioning import MovementProvisioning
from .models.movement_request import MovementRequest
from .models.movement_withdraw import MovementWithdraw


class MovementDonJuanUSDInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un país
    """

    model = MovementDonJuanUsd
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementDailySquareInline(admin.TabularInline):
    """Inline para los movimientos de la caja de un cuadre diario
    """

    model = MovementDailySquare
    extra = 0
    exclude = ('movement_don_juan', 'movement_don_juan_usd', 'movement_partner', 'movement_office', 'movement_cd')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


@admin.register(MovementDailySquare)
class MovementDailySquareAdmin(admin.ModelAdmin):
    """Inline para los movimientos de la caja de un cuadre diario
    """

    list_display = ('box_daily_square', 'date', 'concept', 'detail', 'movement_type', 'value', )
    list_filter = ('box_daily_square', 'concept')
    search_fields = ('box_daily_square__user__first_name',
                     'box_daily_square__user__last_name',
                     )


class MovementDonJuanInline(admin.TabularInline):
    """Inline para los movimientos de la caja de Don Juan
    """

    model = MovementDonJuan
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


@admin.register(MovementDonJuan)
class MovementDonJuan(admin.ModelAdmin):
    """Inline para los movimientos de la caja de Don Juan
    """

    list_display = ('box_don_juan', 'date', 'concept', 'detail', 'value',)
    list_filter = ('box_don_juan__office__office', 'box_don_juan__office', 'concept')


class MovementOfficeInline(admin.TabularInline):
    """Inline para los movimientos de la caja de una oficina
    """

    model = MovementOffice
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})},
    }


class MovementColombiaInline(admin.TabularInline):
    """Inline para los movimientos de la caja Colombia
    """

    model = MovementBoxColombia
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


@admin.register(MovementWithdraw)
class MovementWithdraw(admin.ModelAdmin):

    list_display = ('box_daily_square', 'box_partner', 'date', 'concept', )
    readonly_fields = ('box_daily_square', 'box_partner', 'concept', 'movement_type', 'value', 'detail',
                       'date', 'responsible', 'ip')
    exclude = ('balance', )
