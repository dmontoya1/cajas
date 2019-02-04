from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'webclient'
urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path("create-office-movement/", views.CreateOfficeMovement.as_view(), name='create-office-movement'),
]