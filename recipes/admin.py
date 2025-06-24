from django.contrib import admin
from .models import Recipe, RecipeIngredient
# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug",]
    list_filter = ["category", "cuisine",]
    ordering = ["name",]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    ...
