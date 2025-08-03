from typing import Dict, Any, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .mixins import RecipeListViewMixin, CategoryFilteringMixin
from ingredients.models import UserIngredient
from recipes.models import Recipe, UserRecipe


UserModel = get_user_model()


class IndexView(CategoryFilteringMixin, RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "common/index.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        kwargs.update(
            {
                "search_form": self.form_class(),
                "current_page": "index",
            }
        )

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet[Recipe, Recipe] | QuerySet[Recipe]:
        user = self.request.user

        search_value = self.request.GET.get("query")
        category_value = self.request.GET.get("category")
        category_value = self.request.GET.get("category")
        date_added = self.request.GET.get("date_added")

        added_on_option = "-" if date_added == "on" else ""

        if not user.is_authenticated:
            return Recipe.objects.none()

        user_ingredient_ids = UserIngredient.objects.filter(user=user).values_list(
            "ingredient__id", flat=True
        )

        recipes = Recipe.objects.filter(
            recipe_ingredients__ingredient__in=user_ingredient_ids
        ).distinct()

        user_recipes = UserRecipe.objects.filter(user=user)
        recipes_names = [r.recipe.name for r in user_recipes]

        recipes = recipes.exclude(name__in=recipes_names)

        search_query = Q(name__icontains=search_value) if search_value else Q()

        if category_value == "All" or category_value is None:
            category_query = Q()
        else:
            category_query = Q(category=category_value)

        if search_value or category_value:
            recipes = recipes.filter(search_query, category_query)

        return recipes.order_by(
            f"{added_on_option}added_on",
            "name",
        )


def about_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, "common/about-us.html", context={"current_page": "about_us"})
