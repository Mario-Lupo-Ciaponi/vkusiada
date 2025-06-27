from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from common.forms import SearchForm
from .models import Ingredient


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
