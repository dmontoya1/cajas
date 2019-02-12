from django.urls import path

from . import views

app_name = 'movements'
urlpatterns = [
    path("create-mv-office/", views.MovementOfficeCreate.as_view(), name='movement-create'),
]