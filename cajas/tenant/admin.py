
from django.contrib import admin

from .models import Platform


tenant_admin_site = admin.AdminSite(name="tenant-admin")

admin.site.register(Platform)
tenant_admin_site.register(Platform)
tenant_admin_site.unregister(Platform)
