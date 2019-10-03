from datetime import datetime
from django.contrib import admin

from cajas.general_config.models.exchange import Exchange
from cajas.webclient.views.utils import get_object_or_none

from .models import Loan, LoanHistory
from .models.loan import LoanType
from .services.loan_payment_service import LoanPaymentManager
loan_payment_manager = LoanPaymentManager()


class LoanHistoryStacked(admin.StackedInline):
    """
    """

    model = LoanHistory
    extra = 0


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('provider', 'lender', 'value', 'balance', 'office')
    search_list = ('provider', 'lender')
    search_fields = ('provider__user__first_name', 'provider__user__last_name', 'lender__first_name', 'lender__last_name')
    inlines = [LoanHistoryStacked, ]

    def save_model(self, request, obj, form, change):
        super(LoanAdmin, self).save_model(request, obj, form, change)
        all_payments = obj.related_payments.order_by('date', 'pk')
        if obj.loan_type == LoanType.SOCIO_DIRECTO:
            exchange = get_object_or_none(
                Exchange,
                currency=obj.office.country.currency,
                month__month=datetime.now().month,
            )
            loan_payment_manager.update_all_payments_balance_partner_loan(all_payments, obj, exchange)
        else:
            loan_payment_manager.update_all_payments_balance_employee_loan(all_payments, obj)
        print(obj.balance)
        obj.save()
