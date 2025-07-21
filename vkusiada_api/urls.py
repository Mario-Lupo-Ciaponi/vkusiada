from django.urls import path, include

from . import views


urlpatterns = [
    path(
        "recipe/",
        include(
            [
                path("", views.RecipeView.as_view(), name="all-recipes"),
                path("<int:pk>/", views.RecipeRetrieveView.as_view(), name="recipe"),
            ]
        ),
    ),
    path(
        "ingredient/",
        include(
            [
                path("", views.IngredientListView.as_view(), name="all-ingredients"),
                path(
                    "<int:pk>/",
                    views.IngredientRetrieveView.as_view(),
                    name="ingredient",
                ),
            ]
        ),
    ),
]
