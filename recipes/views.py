from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .models import Recipe
from .forms import CommentForm, CreateRecipeForm, EditRecipeForm, RecipeIngredientFormSet
from .mixins import SlugUrlKwargMixin, FormValidMixin

from common.forms import  SearchForm


class RecipeDetailView(SlugUrlKwargMixin, DetailView, FormMixin):
    model = Recipe
    template_name = "recipes/recipe-details.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            "form": self.get_form_class()(),
        })
        
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy("recipe_details", kwargs={"recipe_slug": self.kwargs.get(self.slug_url_kwarg)})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.username
            comment.recipe = self.object
            comment.save()

            return self.form_valid(form)



class FilteredCategoryView(ListView):
    model = Recipe
    context_object_name = "recipes"
    template_name = "recipes/category-recipes.html"
    query_param = "query"
    paginate_by = 5
    form_class = SearchForm

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "category": self.kwargs.get("category"),
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, "")
        })

        return super().get_context_data(object_list=object_list,**kwargs)

    def get_queryset(self):
        category = self.kwargs.get("category")
        search_value = self.request.GET.get("query")

        category_query = Q(category=category)
        name_query = Q(name__icontains="")

        if search_value:
            name_query = Q(name__icontains=search_value)

        recipes = (Recipe.objects
                   .filter(category_query, name_query)
                   .order_by("name"))

        return recipes


class CreateRecipeView(FormValidMixin, CreateView):
    model = Recipe
    form_class = CreateRecipeForm
    template_name = "recipes/create-recipe.html"

    def get_success_url(self):
        return reverse(
            "recipe_details",
            kwargs={
                "recipe_slug": self.object.slug
            }
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        prefix = 'recipeingredient_set'

        if self.request.POST:
            data["formset"] = RecipeIngredientFormSet(self.request.POST, prefix=prefix)
        else:
            data["formset"] = RecipeIngredientFormSet(prefix=prefix)

        return data


class EditRecipeView(FormValidMixin, UpdateView):
    model = Recipe
    form_class = EditRecipeForm
    template_name = "recipes/edit-recipe.html"
    slug_url_kwarg = "recipe_slug"

    def get_success_url(self):
        return reverse(
            "recipe_details",
            kwargs={
                "recipe_slug": self.object.slug
            }
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        prefix = 'recipeingredient_set'

        if self.request.POST:
            data["formset"] = RecipeIngredientFormSet(
                self.request.POST,
                instance=self.object,
                prefix=prefix
            )
        else:
            data["formset"] = RecipeIngredientFormSet(
                instance=self.object,
                prefix=prefix
            )

        return data


class DeleteRecipeView(SlugUrlKwargMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete-recipe.html"
    success_url = reverse_lazy("index")
