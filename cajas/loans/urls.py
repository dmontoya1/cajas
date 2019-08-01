

from django.urls import path

from .api.views.loan_pay import LoanPaymentCreate
from .api.views.loan_detail import LoanDetail

app_name = 'loans'
urlpatterns = [
    path("add-payment/", LoanPaymentCreate.as_view(), name='loan_payment_create'),
    path("loan/<int:pk>/detail", LoanDetail.as_view(), name='loan_detail'),
]
