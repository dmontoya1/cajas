from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'webclient'
urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("donjuan/<slug:slug>/", views.BoxDonJuanOffice.as_view(), name='box-don-juan'),
    path("partners/", views.PartnerList.as_view(), name='partners-list'),
    path("create-office-movement/", views.CreateOfficeMovement.as_view(), name='create-office-movement'),
]