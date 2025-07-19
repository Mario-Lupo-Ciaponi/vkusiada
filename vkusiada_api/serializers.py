from rest_framework import serializers

from recipes.models import Recipe, RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()
    class Meta:
        model = RecipeIngredient
        exclude = ["id", "recipe",]


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        exclude = ["id", "slug", "users", "ingredients",]

