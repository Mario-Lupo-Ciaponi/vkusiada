from django.urls import path, include
from ingredients import views


urlpatterns = [
    path("add-ingredient/", views.AddIngredientView.as_view(), name="add-ingredient"),
    path("saved-ingredients/", views.SavedIngredientsView.as_view(), name="saved-ingredient"),
    path("save/<int:ingredient_pk>/", views.save_ingredient, name="save-ingredient"),
    path("<slug:ingredient_slug>/", views.IngredientDetailsView.as_view(), name="ingredient-details"),
]