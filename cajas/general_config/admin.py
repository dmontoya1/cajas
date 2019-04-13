import re
from datetime import datetime

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

    def has_change_permission(self, request, obj=None):
        validator = True
        if request.method == "POST":
            for i in range(int(request.POST["exchange_set-INITIAL_FORMS"])):
                date = re.split(r'\/', request.POST["exchange_set-"+str(i)+"-month"])
                if date[1] == '{:02d}'.format(datetime.today().month):
                    if '{:02d}'.format(datetime.today().day) == '01':
                        validator = True
                    else:
                        validator = False
                else:
                    validator = False
            return validator
        return True


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):

    model = Currency
    list_display = ['name', 'abbr']
    inlines = [ExchangeAdmin, ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    model = Country
    list_display = ['name', 'abbr', 'currency']
