from django.contrib import admin

from . import models


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...


# Primeira forma de registrar na zona administrativa
admin.site.register(models.Category, CategoryAdmin)

# segunda forma registrar na zna administrativa


@admin.register(models.Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }
