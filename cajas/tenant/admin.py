
from django.db import connection
from django.contrib import admin

from .models import Platform


# @admin.register(Platform)
class TenantAdmin(admin.ModelAdmin):

    list_display = ('name', 'schema_name', 'domain_url')

    def get_queryset(self, request):
        schema_name = connection.schema_name
        if schema_name == 'public':
            return super(TenantAdmin, self).get_queryset(request)
        return []
