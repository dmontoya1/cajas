from django.contrib import admin

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

from general_config.models.country import Country
from general_config.models.currency import Currency
from general_config.models.exchange import Exchange

admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)


class ExchangeAdmin(admin.StackedInline):

    model = Exchange
    extra = 0


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):

    model = Currency
    list_display = ['name', 'abbr']
    inlines = [ExchangeAdmin, ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    model = Country
    list_display = ['name', 'abbr', 'currency']
