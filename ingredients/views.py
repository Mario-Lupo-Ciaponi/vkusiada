from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from common.forms import SearchForm
from .models import Ingredient, UserIngredient


class IngredientDetailsView(DetailView):
    model = Ingredient
    template_name = "ingredients/ingredients-details.html"
    context_object_name = "ingredient"
    slug_url_kwarg = "ingredient_slug"


class AddIngredientView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "ingredients/add-ingredient.html"
    query_param = "query"
    paginate_by = 7
    form_class = SearchForm

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, ""),
        })

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet:
        search_value = self.request.GET.get("query")

        if search_value:
            ingredients = Ingredient.objects.filter(name__icontains=search_value)
        else:
            ingredients = Ingredient.objects.all()

        return ingredients.order_by("name")


def save_ingredient(request: HttpRequest, ingredient_pk: int) -> HttpResponse:
    ingredient = Ingredient.objects.get(pk=ingredient_pk)
    user = request.user

    UserIngredient.objects.create(
        ingredient=ingredient,
        user=user,
        added_on=now
    )

    return redirect("add-ingredient")
