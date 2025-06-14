from django.shortcuts import render
from django.views.generic import DetailView

from .models import Ingredient


class IngredientDetailsView(DetailView):
    model = Ingredient
    template_name = "ingredients/ingredients-details.html"
    context_object_name = "ingredient"
    slug_url_kwarg = "ingredient_slug"
