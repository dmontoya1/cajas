
from django.urls import path

from .api.views.investment_create import InvestmentCreate

app_name = 'investments'
urlpatterns = [
    path("create/", InvestmentCreate.as_view(), name='create'),
]
