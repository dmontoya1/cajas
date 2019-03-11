

from django.urls import path

from .api.sell_unit import UnitSell
from .api.unit_detail import UnitDetail
from .api.unit_list import UnitList

app_name = 'units'
urlpatterns = [
    path("<int:pk>/detail", UnitDetail.as_view(), name='unit-detail'),
    path("<int:pk>/list", UnitList.as_view(), name='unit-list'),
    path("sell/", UnitSell.as_view(), name='unit_sell'),
]
