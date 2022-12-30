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
    ...
