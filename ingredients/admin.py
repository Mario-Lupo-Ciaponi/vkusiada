from django.contrib import admin

from .models import Ingredient, UserIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "number_of_recipes_used_in",]
    search_fields = ["name",]

    @admin.display
    def number_of_recipes_used_in(self, obj):
        return obj.recipeingredient_set.count()


@admin.register(UserIngredient)
class UserIngredientAdmin(admin.ModelAdmin):
    list_display = ["ingredient", "user",]
