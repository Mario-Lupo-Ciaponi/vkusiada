from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from recipes.models import Recipe
from vkusiada_api.serializers import RecipeSerializer


class RecipeView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeRetrieveView(RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
