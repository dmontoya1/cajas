from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'movements'
urlpatterns = [
    path("create-mv-office/", views.MovementOfficeCreate.as_view(), name='movement-create'),
]