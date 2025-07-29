from django.urls import path, include
from ingredients import views


urlpatterns = [
    path("add-ingredient/", views.AddIngredientView.as_view(), name="add-ingredient"),
    path(
        "saved-ingredients/",
        views.SavedIngredientsView.as_view(),
        name="saved-ingredients",
    ),
    path(
        "<int:ingredient_pk>/",
        include(
            [
                path("save/", views.save_ingredient, name="save-ingredient"),
                path("remove/", views.remove_ingredient, name="remove-ingredient"),
            ]
        ),
    ),
    path(
        "<slug:ingredient_slug>/",
        views.IngredientDetailsView.as_view(),
        name="ingredient-details",
    ),
]
