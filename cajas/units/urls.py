

from django.urls import path

from .api.views.unit_create import UnitCreate
from .api.views.unit_detail import UnitDetail
from .api.views.unit_delete import UnitDelete
from .api.views.unit_list import UnitList
from .api.views.sell_unit import UnitSell

app_name = 'units'
urlpatterns = [
    path("unit-create", UnitCreate.as_view(), name='unit_create'),
    path("<int:pk>/detail", UnitDetail.as_view(), name='unit_detail'),
    path("<int:pk>/delete", UnitDelete.as_view(), name='unit_delete'),
    path("<int:pk>/list", UnitList.as_view(), name='unit_list'),
    path("sell/", UnitSell.as_view(), name='unit_sell'),
]
