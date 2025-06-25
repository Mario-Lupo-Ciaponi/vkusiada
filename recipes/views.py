from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from .models import Recipe
from .forms import CommentForm, CreateRecipeForm, EditRecipeForm, RecipeIngredientFormSet
from common.forms import  SearchForm


class RecipeDetailView(DetailView, FormMixin):
    model = Recipe
    template_name = "recipes/recipe-details.html"
    slug_url_kwarg = "recipe_slug"
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


class CreateRecipeView(CreateView):
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
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()  # handles deletions!
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))


class EditRecipeView(UpdateView):
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

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        # Print for debugging (optional)
        print("Form is valid?", form.is_valid())
        print("Formset is valid?", formset.is_valid())
        print("Formset errors:", formset.errors)

        # Clear id field value for new forms (to avoid "This field is required" error)
        # But cleaned_data only exists after is_valid(), so do this inside clean() or rely on JS fix below.

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()  # handles deletions!
            return redirect(self.get_success_url())

        print("Formset is invalid, re-rendering form")
        return self.render_to_response(self.get_context_data(form=form))