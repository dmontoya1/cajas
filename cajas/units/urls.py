

from django.urls import path

from .views.unit.unit_detail import UnitDetail
from .views.unit.unit_list import UnitList

app_name = 'units'
urlpatterns = [
    path(
        "<int:pk>/detail",
        UnitDetail.as_view(),
        name='unit-detail'
    ),
    path(
        "<int:pk>/list",
        UnitList.as_view(),
        name='unit-list'
    ),
]
