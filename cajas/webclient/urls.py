from django.conf import settings
from django.urls import include, path

from . import views

app_name = 'webclient'
urlpatterns = [
    path("", views.Home.as_view(), name='home'),
]