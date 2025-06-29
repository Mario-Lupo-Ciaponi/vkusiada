from django.contrib import admin
from .models import Recipe, RecipeIngredient, Comment


# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug",]
    list_filter = ["category", "cuisine",]
    ordering = ["name",]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...

