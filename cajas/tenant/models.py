from django.db import models
from tenant_schemas.models import TenantMixin
# from tenant_users.tenants.models import TenantBase


class Platform(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return "Plataforma {}".format(self.name)

    class Meta:
        verbose_name = 'Plataforma'
