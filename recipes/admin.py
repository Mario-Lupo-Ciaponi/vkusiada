from django.contrib import admin
from .models import User, Ingredient, Recipe, RecipeIngredient
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]
    list_filter = ["category", "cuisine"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    ...
