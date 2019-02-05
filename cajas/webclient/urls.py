from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'webclient'
urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("donjuan/<slug:slug>/", views.BoxDonJuanOffice.as_view(), name='box-don-juan'),
    path("partners/", views.PartnerList.as_view(), name='partners-list'),
    path("daily-square/", views.DailySquareList.as_view(), name='daily-square-list'),
    path("partner/add/", views.PartnerCreate.as_view(), name='partner-add'),
    path("partner/<int:pk>/box/", views.PartnerBox.as_view(), name='partner-box'),
    path("daily-square/<int:pk>/box/", views.DailySquareBox.as_view(), name='daily-square-box'),
    path("create-office-movement/", views.CreateOfficeMovement.as_view(), name='create-office-movement'),
    path("create-partner-movement/", views.CreatePartnerMovement.as_view(), name='add-partner-movement'),
    path("create-daily-square-movement/", views.CreateDailySquareMovement.as_view(), name='add-daily-square-movement'),
]