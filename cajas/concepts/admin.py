from django.contrib import admin

from concepts.models.concepts import Concept
from concepts.models.stops import Stop


class StopAdmin(admin.StackedInline):

    model = Stop
    extra = 0


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):

    list_display = ['name', 'concept_type', 'counterpart_name']
    search_fields = ['name', 'counterpart_name, relationship']
    inlines = [StopAdmin, ]
