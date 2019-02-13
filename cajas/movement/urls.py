from django.urls import path

from .views import movement_don_juan
from .views.movement_office import movement_office_create

app_name = 'movements'
urlpatterns = [
    path(
        "create-mv-office/",
        movement_office_create.MovementOfficeCreate.as_view(),
        name='movement-create'
    ),
]