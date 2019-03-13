from django.contrib import admin

from .models.loan import Loan
from .models.loan_payments import LoanPayment


class LoanPaymentStacked(admin.StackedInline):
    """
    """

    model = LoanPayment
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('provider', 'lender', 'value', 'balance')
    search_list = ('provider', 'lender')
    search_fields = ('provider__first_name', 'provider__last_name', 'lender__first_name', 'lender__last_name')
    inlines = [LoanPaymentStacked, ]
