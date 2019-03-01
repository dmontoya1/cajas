from django.conf import settings
from django.urls import include, path

from .views.box_don_juan_office import BoxDonJuanOffice
from .views.create_daily_square_movement import CreateDailySquareMovement
from .views.create_office_movement import CreateOfficeMovement
from .views.create_partner_movement import CreatePartnerMovement
from .views.daily_square_box import DailySquareBox
from .views.daily_square_list import DailySquareList
from .views.home_view import Home
from .views.office_box import OfficeBox
from .views.partner_box import PartnerBox
from .views.partner_create import PartnerCreate
from .views.partner_list import PartnerList

app_name = 'webclient'
urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("office/<slug:slug>/", OfficeBox.as_view(), name='office'),
    path("office/<slug:slug>/donjuan/", BoxDonJuanOffice.as_view(), name='box_don_juan'),
    path("office/<slug:slug>/partners/", PartnerList.as_view(), name='partners_list'),
    path("office/<slug:slug>/daily-square/", DailySquareList.as_view(), name='daily_square_list'),
    path("partner/add/", PartnerCreate.as_view(), name='partner_add'),
    path("office/<slug:slug>/partner/<int:pk>/box/", PartnerBox.as_view(), name='partner_box'),
    path("office/<slug:slug>/daily-square/<int:pk>/box/", DailySquareBox.as_view(), name='daily_square_box'),
    path("office/<slug:slug>/create_office_movement/", CreateOfficeMovement.as_view(), name='create_office_movement'),
    path("office/<slug:slug>/create-partner-movement/", CreatePartnerMovement.as_view(), name='add_partner_movement'),
    path("create-daily-square-movement/", CreateDailySquareMovement.as_view(), name='add_daily_square_movement'),
]
