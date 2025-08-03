from typing import Dict, Any

import psycopg2.errors
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, CreateView
from django.contrib import messages
from rest_framework.reverse import reverse_lazy

from common.forms import SearchForm
from .forms import IngredientAddForm
from .models import Ingredient, UserIngredient


class IngredientDetailsView(DetailView):
    model = Ingredient
    template_name = "ingredients/ingredients-details.html"
    context_object_name = "ingredient"
    slug_url_kwarg = "ingredient_slug"


class BrowseIngredients(ListView):
    model = Ingredient
    template_name = "ingredients/browse-ingredients.html"
    query_param = "query"
    paginate_by = 7
    form_class = SearchForm

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
            }
        )

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet[Ingredient, Ingredient] | QuerySet[Ingredient]:
        search_value = self.request.GET.get("query")
        user = self.request.user

        if not user.is_authenticated:
            return Ingredient.objects.all()

        ingredients_added = UserIngredient.objects.filter(user=user)
        ingredients_name = [i.ingredient.name for i in ingredients_added]

        ingredients_query = ~Q(
            name__in=ingredients_name
        )  # Filters ingredients where the name is NOT present in ingredients_name

        if search_value:
            ingredients_query &= Q(
                name__icontains=search_value
            )  # Search value is the value of the search form

        ingredients = Ingredient.objects.filter(ingredients_query)

        return ingredients.order_by("name")


class AddIngredient(CreateView):
    model = Ingredient
    form_class = IngredientAddForm
    template_name = "ingredients/add-ingredient.html"
    success_url = reverse_lazy("browse-ingredients")


class SavedIngredientsView(LoginRequiredMixin, ListView):
    model = UserIngredient
    template_name = "ingredients/saved-ingredients.html"
    query_param = "query"
    paginate_by = 7
    form_class = SearchForm
    context_object_name = "ingredients"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
            }
        )

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> list[UserIngredient]:
        search_value = self.request.GET.get("query")
        user = self.request.user

        saved_ingredients = UserIngredient.objects.filter(user=user)

        if search_value:
            saved_ingredients = saved_ingredients.filter(
                ingredient__name__icontains=search_value
            )

        saved_ingredients = saved_ingredients.order_by("ingredient__name")

        return [i for i in saved_ingredients]


@require_POST
@login_required
def save_ingredient(request: HttpRequest, ingredient_pk: int) -> HttpResponse:
    ingredient = Ingredient.objects.get(pk=ingredient_pk)
    user = request.user

    try:
        with transaction.atomic():
            UserIngredient.objects.create(
                ingredient=ingredient, user=user, added_on=now()
            )
            messages.success(request, f"{ingredient} added successfully!")
    except IntegrityError:
        messages.error(request, f"{ingredient} already added!")

    return redirect("browse-ingredients")


@require_POST
@login_required
def remove_ingredient(request: HttpRequest, ingredient_pk: int) -> HttpResponse:
    user_ingredient = get_object_or_404(
        UserIngredient, pk=ingredient_pk, user=request.user
    )

    user_ingredient.delete()

    messages.success(
        request,
        f"Ingredient {user_ingredient.ingredient.name} was removed successfully",
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))
