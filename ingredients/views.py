from typing import Dict, Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.generic import DetailView, ListView
from django.contrib import messages

from common.forms import SearchForm
from .models import Ingredient, UserIngredient


class IngredientDetailsView(DetailView):
    model = Ingredient
    template_name = "ingredients/ingredients-details.html"
    context_object_name = "ingredient"
    slug_url_kwarg = "ingredient_slug"


class AddIngredientView(ListView):
    model = Ingredient
    template_name = "ingredients/add-ingredient.html"
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

        return [i for i in saved_ingredients]


@login_required
def save_ingredient(request: HttpRequest, ingredient_pk: int) -> HttpResponse:
    ingredient = Ingredient.objects.get(pk=ingredient_pk)
    user = request.user

    UserIngredient.objects.create(ingredient=ingredient, user=user, added_on=now())

    return redirect("add-ingredient")


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
