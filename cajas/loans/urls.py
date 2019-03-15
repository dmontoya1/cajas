

from django.urls import path

from .api.loan_pay import LoanPaymentCreate

app_name = 'loans'
urlpatterns = [
    path("add-payment/", LoanPaymentCreate.as_view(), name='loan_payment_create'),
]
