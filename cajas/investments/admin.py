
from django.contrib import admin

from .models.investment import Investment
from .models.investment_pay import InvestmentPay


class InvestmentPayStacked(admin.StackedInline):

    model = InvestmentPay
    extra = 0


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):

    list_display = ('partner', 'date', 'element', 'total_value')
    inlines = [InvestmentPayStacked]
