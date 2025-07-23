from pyperclip import copy
from typing import Dict, Any

import django.db.utils
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, resolve_url
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormMixin
from django.contrib import messages

from common.models import Like
from .models import Recipe, Comment, UserRecipe
from .forms import (
    AddCommentForm,
    CreateRecipeForm,
    EditRecipeForm,
    RecipeIngredientFormSet,
    EditCommentForm,
)
from .mixins import (
    SlugUrlKwargMixin,
    FormValidMixin,
    TestFuncMixin,
    TestFuncCommentMixin,
)
from common.mixins import CategoryFilteringMixin, RecipeListViewMixin

from common.forms import SearchForm


UserModel = get_user_model()


class RecipeDetailView(SlugUrlKwargMixin, DetailView, FormMixin):
    model = Recipe
    template_name = "recipes/recipe-details.html"
    form_class = AddCommentForm

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        It adds into the context form(search form), total_likes and has_user_liked.
        It filters like to see if the user has liked the recipe, then checks whether
        the user is authenticated, because a anonymous user cannot like recipes, he/she
        must login first.
        """
        user = self.request.user
        has_user_liked = False

        if self.request.user.is_authenticated:
            like = Like.objects.filter(user=user, recipe=self.object)

            if like:
                has_user_liked = True

        kwargs.update(
            {
                "form": self.get_form_class()(),
                "total_likes": Like.objects.filter(recipe=self.object).count(),
                "has_user_liked": has_user_liked,
            }
        )

        return super().get_context_data(**kwargs)

    def get_success_url(self) -> HttpResponseRedirect:
        """
        It gets dynamically the url, because based on the query params the recipe name can vary.
        """
        return reverse_lazy(
            "recipe_details",
            kwargs={"recipe_slug": self.kwargs.get(self.slug_url_kwarg)},
        )

    def post(self, request, *args, **kwargs) -> HttpResponse | None:
        """
        It handles the post request for adding a comment to the recipe.
        """
        self.get_success_url()
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = self.get_form_class()(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.recipe = self.object
                comment.save()

                return self.form_valid(form)

        return redirect("login")


class FilteredCategoryView(RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "recipes/category-recipes.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        """
        It updates the context with the search form and the query parameter.
        """
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
            }
        )

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet[Recipe]:
        """
        It filters the recipes based on the category and the search value.
        If the search value is provided, it filters the recipes by name.
        """
        category = self.kwargs.get("category")
        search_value = self.request.GET.get("query")

        category_query = Q(category=category)
        name_query = Q(name__icontains="")

        if search_value:
            name_query = Q(name__icontains=search_value)

        recipes = Recipe.objects.filter(category_query, name_query).order_by("name")

        return recipes


class SavedRecipesView(LoginRequiredMixin, CategoryFilteringMixin, ListView):
    model = UserRecipe
    template_name = "recipes/saved-recipes.html"
    paginate_by = 5
    query_param = "query"
    form_class = SearchForm
    context_object_name = "recipes"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        """
        It updates the context with the search form and the query parameter.
        This method is called when rendering the template.
        """
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
            }
        )

        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet[UserRecipe]:
        """
        It retrieves the saved recipes for the logged-in user.
        It filters the recipes based on the search value and category value.
        """
        # Get the user once
        user = self.request.user

        search_value = self.request.GET.get("query")
        category_value = self.request.GET.get("category")

        search_query = Q(recipe__name__icontains=search_value)
        category_query = Q(recipe__category=category_value)

        users_recipes = UserRecipe.objects.filter(user=user).order_by("recipe__name")

        if search_value or category_value:
            users_recipes = users_recipes.filter(search_query, category_query)

        return users_recipes


class SearchRecipeView(CategoryFilteringMixin, RecipeListViewMixin, ListView):
    model = Recipe
    template_name = "recipes/search-recipe.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        """
        It updates the context with the search form and the query parameter.
        This method is called when rendering the template.
        """
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
            }
        )
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        """
        It retrieves the recipes based on the search value and category value.
        If the user is authenticated, it excludes the recipes that the user has already saved.
        It filters the recipes based on the search value and category value.
        If the search value or category value is provided, it filters the recipes by name and category.
        """
        user = self.request.user

        search_value = self.request.GET.get("query")
        category_value = self.request.GET.get("category")
        recipes = Recipe.objects.order_by("name")

        search_query = Q(name__icontains=search_value)
        category_query = Q(category=category_value)

        if search_value or category_value:
            recipes = recipes.filter(search_query, category_query)

        if user.is_authenticated:
            user_recipes = UserRecipe.objects.filter(user=user)
            recipes_names = [r.recipe.name for r in user_recipes]

            recipes = recipes.exclude(name__in=recipes_names)

        return recipes


class RecipesCreatedByUserView(ListView):
    model = Recipe
    template_name = "recipes/recipes-created.html"
    paginate_by = 5
    query_param = "query"
    form_class = SearchForm
    context_object_name = "recipes"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        """
        It updates the context with the search form, query parameter, and author.
        """
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
                "author": get_object_or_404(UserModel, pk=self.kwargs.get("user_pk")),
            }
        )
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self) -> QuerySet[Recipe]:
        """
        It retrieves the recipes created by a specific user.
        It filters the recipes based on the search value.
        """
        user_pk = self.kwargs.get("user_pk")

        search_value = self.request.GET.get("query")
        recipes = Recipe.objects.filter(author__pk=user_pk).order_by("name")

        if search_value:
            recipes = recipes.filter(name__icontains=search_value)

        return recipes


class CreateRecipeView(LoginRequiredMixin, FormValidMixin, CreateView):
    model = Recipe
    form_class = CreateRecipeForm
    template_name = "recipes/create-recipe.html"

    def get_success_url(self) -> str:
        """
        It gets the success URL after creating a recipe.
        """
        return reverse("recipe_details", kwargs={"recipe_slug": self.object.slug})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        It prepares the context data for the recipe creation view.
        It initializes a formset for recipe ingredients and adds it to the context.
        If the request is a POST request, it populates the formset with the submitted data.
        If it's a GET request, it initializes an empty formset.
        """

        data = super().get_context_data(**kwargs)
        prefix = "recipeingredient_set"

        if self.request.POST:
            data["formset"] = RecipeIngredientFormSet(self.request.POST, prefix=prefix)
        else:
            data["formset"] = RecipeIngredientFormSet(prefix=prefix)

        return data

    def form_valid(self, form) -> HttpResponse:
        """
        It handles the form validation for creating a recipe.
        It sets the author of the recipe to the current user before saving.
        """

        form.instance.author = self.request.user
        return super().form_valid(form)


class EditRecipeView(
    LoginRequiredMixin, FormValidMixin, TestFuncMixin, UserPassesTestMixin, UpdateView
):
    model = Recipe
    form_class = EditRecipeForm
    template_name = "recipes/edit-recipe.html"
    slug_url_kwarg = "recipe_slug"

    def get_success_url(self) -> str:
        """
        It gets the success URL after editing a recipe.
        """

        return reverse("recipe_details", kwargs={"recipe_slug": self.object.slug})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        It prepares the context data for the recipe editing view.
        It initializes a formset for recipe ingredients and adds it to the context.
        If the request is a POST request, it populates the formset with the submitted data.
        If it's a GET request, it initializes an empty formset.
        """

        data = super().get_context_data(**kwargs)
        prefix = "recipeingredient_set"

        if self.request.POST:
            data["formset"] = RecipeIngredientFormSet(
                self.request.POST, instance=self.object, prefix=prefix
            )
        else:
            data["formset"] = RecipeIngredientFormSet(
                instance=self.object, prefix=prefix
            )

        return data


class DeleteRecipeView(
    LoginRequiredMixin,
    SlugUrlKwargMixin,
    TestFuncMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Recipe
    template_name = "recipes/delete-recipe.html"
    success_url = reverse_lazy("index")


class EditCommentView(
    LoginRequiredMixin, TestFuncCommentMixin, UserPassesTestMixin, UpdateView
):
    model = Comment
    template_name = "recipes/edit-comment.html"
    form_class = EditCommentForm

    def get_success_url(self) -> str:
        """
        It gets the success URL after editing a comment.
        """

        return reverse(
            "recipe_details",
            kwargs={
                "recipe_slug": self.object.recipe.slug,
            },
        )


class DeleteCommentView(
    LoginRequiredMixin, TestFuncCommentMixin, UserPassesTestMixin, DeleteView
):
    model = Comment
    template_name = "recipes/delete-recipe.html"

    def get_success_url(self) -> str:
        """
        It gets the success URL after deleting a comment.
        """
        return reverse(
            "recipe_details",
            kwargs={
                "recipe_slug": self.object.recipe.slug,
            },
        )


@login_required
def save_recipe(request: HttpRequest, recipe_slug) -> HttpResponse:
    """
    It saves a recipe for the logged-in user.
    If the recipe is already saved, it shows a warning message.
    """

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
    """
    It removes a saved recipe for the logged-in user.
    """

    recipe = Recipe.objects.get(slug=recipe_slug)
    user_recipe = get_object_or_404(UserRecipe, recipe=recipe, user=request.user)

    user_recipe.delete()

    messages.success(
        request, f"Recipe {user_recipe.recipe.name} was removed successfully"
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))


def like_recipe(request: HttpRequest, recipe_slug: str, user_pk) -> HttpResponse:
    """
    It toggles the like status of a recipe for a specific user.
    If the user has already liked the recipe, it removes the like.
    If the user has not liked the recipe, it creates a new like.
    """
    recipe = Recipe.objects.get(slug=recipe_slug)
    user = UserModel.objects.get(pk=user_pk)

    like = Like.objects.filter(
        recipe=recipe,
        user=user,
    )

    if like:
        like.first().delete()
    else:
        Like.objects.create(
            recipe=recipe,
            user=user,
        )

    return redirect(request.META.get("HTTP_REFERER", "/"))


def copy_recipe_link(request: HttpResponse, recipe_slug) -> HttpResponse:
    """
    It copies the recipe link to the clipboard.
    """

    copy(request.META.get("HTTP_REFERER", "/"))

    return redirect(request.META.get("HTTP_REFERER", "/"))
