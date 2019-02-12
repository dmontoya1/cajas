from django.contrib import admin

from inventory.models.category import Category
from inventory.models.brand import Brand


class BrandAdmin(admin.StackedInline):
    """
    """

    model = Brand
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    """

    list_display = ('name', )
    search_fields = ('name', )
    inlines = [BrandAdmin, ]
