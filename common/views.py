from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from ingredients.models import UserIngredient
from recipes.mixins import RecipeListViewMixin
from recipes.models import Recipe, UserRecipe

UserModel = get_user_model()

class IndexView(RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "common/index.html"

    def get_context_data(
            self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, ""),
            "current_page": "index",
        })

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get("query")

        if not user.is_authenticated:
            return UserModel.objects.none()

        user_ingredient_ids = (UserIngredient.objects
                               .filter(user=user)
                               .values_list("ingredient__id", flat=True))

        recipes = (Recipe.objects
                  .filter(recipeingredient__ingredient__in=user_ingredient_ids)
                  .distinct())

        user_recipes = UserRecipe.objects.filter(user=user)
        recipes_names = [r.recipe.name for r in user_recipes]

        recipes = recipes.exclude(name__in=recipes_names)

        if search_query:
            recipes = recipes.filter(name__icontains=search_query)

        return recipes

def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, "common/index.html", context={"current_page": "index"})


def about_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, "common/about-us.html", context={"current_page": "about_us"})