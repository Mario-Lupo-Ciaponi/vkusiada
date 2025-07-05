import django.db.utils
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib import messages

from ingredients.models import UserIngredient
from .models import Recipe, UserRecipe
from .forms import CommentForm, CreateRecipeForm, EditRecipeForm, RecipeIngredientFormSet
from .mixins import SlugUrlKwargMixin, FormValidMixin, RecipeListViewMixin, TestFuncMixin

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
            comment.author = request.user
            comment.recipe = self.object
            comment.save()

            return self.form_valid(form)


class SuggestedRecipesView(LoginRequiredMixin, RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "recipes/suggested-recipes.html"

    def get_context_data(
            self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, "")
        })

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        user = self.request.user

        user_ingredient_ids = (UserIngredient.objects
                               .filter(user=user)
                               .values_list("ingredient__id", flat=True))

        recipe = (Recipe.objects
                  .filter(recipeingredient__ingredient__in=user_ingredient_ids)
                  .distinct())

        return recipe


class FilteredCategoryView(RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "recipes/category-recipes.html"

    def get_context_data(
            self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "category": self.kwargs.get("category"),
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, "")
        })

        return super().get_context_data(object_list=object_list, **kwargs)

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


class SavedRecipesView(LoginRequiredMixin, ListView):
    model = UserRecipe
    template_name = "recipes/saved-recipes.html"
    paginate_by = 5
    query_param = "query"
    form_class = SearchForm
    context_object_name = "recipes"

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, "")
        })

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        # Get the user once
        user = self.request.user
        query = self.request.GET.get("query")

        users_recipes = UserRecipe.objects.filter(user=user).order_by("recipe__name")

        if query:
            users_recipes = users_recipes.filter(recipe__name__icontains=query)

        return users_recipes


class SearchRecipeView(ListView):
    model = Recipe
    paginate_by = 5
    template_name = "recipes/search-recipe.html"
    query_param = "query"
    form_class = SearchForm
    context_object_name = "recipes"

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        kwargs.update({
            "search_form": self.form_class(),
            "query": self.request.GET.get(self.query_param, "")
        })
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        search_value = self.request.GET.get("query")
        recipes = Recipe.objects.order_by("name")

        if search_value:
            recipes = recipes.filter(name__icontains=search_value)

        return recipes


class CreateRecipeView(LoginRequiredMixin, FormValidMixin, CreateView):
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditRecipeView(FormValidMixin, TestFuncMixin, UserPassesTestMixin, UpdateView):
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


class DeleteRecipeView(SlugUrlKwargMixin, TestFuncMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete-recipe.html"
    success_url = reverse_lazy("index")


@login_required
def save_recipe(request: HttpRequest, recipe_slug) -> HttpResponse:
    recipe = Recipe.objects.get(slug=recipe_slug)
    user = request.user

    try:
        UserRecipe.objects.create(
            user=user,
            recipe=recipe,
            added_on=now,
        )
    except django.db.utils.IntegrityError:
        messages.warning(request, "You already saved the recipe!")

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_saved_recipe(request: HttpRequest, recipe_slug: str) -> HttpResponse:
    recipe = Recipe.objects.get(slug=recipe_slug)
    user_recipe = get_object_or_404(UserRecipe, recipe=recipe, user=request.user)

    user_recipe.delete()

    messages.success(request, f"Recipe {user_recipe.recipe.name} was removed successfully")

    return redirect(request.META.get("HTTP_REFERER", "/"))

