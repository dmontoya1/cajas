from django.urls import path

from .api.views.provisioning_create import ProvisioningCreate
from .api.views.provisioning_detail import ProvisioningDetail

app_name = 'boxes'
urlpatterns = [
    path("provisioning-create", ProvisioningCreate.as_view(), name='provisioning_create'),
    path("<int:pk>/privisioning-detail", ProvisioningDetail.as_view(), name='provisioning_detail'),
]
