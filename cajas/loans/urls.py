

from django.urls import path

from cajas.loans.api.views.loan_pay import LoanPaymentCreate
from cajas.loans.api.views.loan_detail import LoanDetail

app_name = 'loans'
urlpatterns = [
    path("add-payment/", LoanPaymentCreate.as_view(), name='loan_payment_create'),
    path("loan/<int:pk>/detail", LoanDetail.as_view(), name='loan_detail'),
]
