from django.contrib import admin

from .models import Loan, LoanHistory


class LoanHistoryStacked(admin.StackedInline):
    """
    """

    model = LoanHistory
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('provider', 'lender', 'value', 'balance')
    search_list = ('provider', 'lender')
    search_fields = ('provider__user__first_name', 'provider__user__last_name', 'lender__first_name', 'lender__last_name')
    inlines = [LoanHistoryStacked, ]
