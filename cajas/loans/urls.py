
from django.urls import path

from .api.views.loan_pay import LoanPaymentCreate
from .api.views.loan_detail import LoanDetail
from .api.views.loan_history_detail import LoanHistoryDetail

app_name = 'loans'
urlpatterns = [
    path("add-payment/", LoanPaymentCreate.as_view(), name='loan_payment_create'),
    path("loan/<int:pk>/detail", LoanDetail.as_view(), name='loan_detail'),
    path("loan-history/<int:pk>/detail", LoanHistoryDetail.as_view(), name='loan_history_detail'),
]
