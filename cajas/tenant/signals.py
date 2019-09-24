
from tenant_schemas.signals import post_schema_sync
from tenant_schemas.utils import tenant_context
from tenant_schemas.models import TenantMixin

from cajas.tenant.models import Platform
from cajas.users.models.user import User


def after_schema_is_created(sender, tenant, **kwargs):
    print("Se acabó de crear un Schema")
    print(tenant.schema_name)
    tenant1 = Platform(schema_name=tenant.schema_name)  # "Client" is a tenant model

    with tenant_context(tenant1):
        email = '{}@sac.com'.format(tenant.schema_name)
        User.objects.create_superuser(username='super_admin', password='globalsac', email=email)


post_schema_sync.connect(after_schema_is_created, sender=TenantMixin)
