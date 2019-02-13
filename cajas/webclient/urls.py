from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'webclient'
urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("donjuan/", views.BoxDonJuanOffice.as_view(), name='box_don_juan'),
    path("partners/", views.PartnerList.as_view(), name='partners_list'),
    path("daily-square/", views.DailySquareList.as_view(), name='daily_square_list'),
    path("partner/add/", views.PartnerCreate.as_view(), name='partner_add'),
    path("partner/<int:pk>/box/", views.PartnerBox.as_view(), name='partner_box'),
    path("daily-square/<int:pk>/box/", views.DailySquareBox.as_view(), name='daily_square_box'),
    path("create_office_movement/", views.CreateOfficeMovement.as_view(), name='create_office_movement'),
    path("create-partner-movement/", views.CreatePartnerMovement.as_view(), name='add_partner_movement'),
    path("create-daily-square-movement/", views.CreateDailySquareMovement.as_view(), name='add_daily_square_movement'),
]