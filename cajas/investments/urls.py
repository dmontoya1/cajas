
from django.urls import path

from .api.views.investment_create import InvestmentCreate
from .api.views.investment_pay_create import InvestmentPayCreate

app_name = 'investments'
urlpatterns = [
    path("create/", InvestmentCreate.as_view(), name='create'),
    path("pay-create/", InvestmentPayCreate.as_view(), name='pay_create'),
]
