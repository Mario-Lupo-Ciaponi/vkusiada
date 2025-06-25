from django.urls import path, include
from recipes import views
urlpatterns = [
    path("create/", views.CreateRecipeView.as_view(), name="create-recipe"),
    path("<slug:recipe_slug>/", include([
        path("details/", views.RecipeDetailView.as_view(), name="recipe_details"),
        path("edit/", views.EditRecipeView.as_view(), name="edit-recipe"),
    ])),
    path("category/<str:category>/", views.FilteredCategoryView.as_view(), name="category_recipes"),
]