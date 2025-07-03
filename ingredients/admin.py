from django.contrib import admin

from .models import Ingredient, UserIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name",]


@admin.register(UserIngredient)
class UserIngredientAdmin(admin.ModelAdmin):
    ...
