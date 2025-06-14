from django.urls import path, include
from recipes import views
urlpatterns = [
    path("recipe/", include([
        path("<slug:recipe_slug>/", views.RecipeDetailView.as_view(), name="recipe_details"),
        path("category/<str:category>/", views.FilteredCategoryView.as_view(), name="category_recipes"),
    ])),
]