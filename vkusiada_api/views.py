from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from ingredients.models import Ingredient
from recipes.models import Recipe
from vkusiada_api.serializers import RecipeSerializer, IngredientSerializer


class RecipeView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeRetrieveView(RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientListView(ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientRetrieveView(RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
