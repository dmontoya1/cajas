from django.contrib import admin

from concepts.models.concepts import Concept
from concepts.models.stops import Stop


class StopAdmin(admin.StackedInline):

    model = Stop
    extra = 0


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):

    list_display = ['name', 'concept_type', 'counterpart']
    search_fields = ['name', 'counterpart__name']
    inlines = [StopAdmin, ]

    class Media:
        js = (
            'js/admin/concept_admin.js',
        )
