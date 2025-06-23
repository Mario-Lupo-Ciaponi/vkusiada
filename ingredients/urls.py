from django.urls import path, include
from ingredients import views


urlpatterns = [
    path("add-ingredient/", views.AddIngredientView.as_view(), name="add-ingredient"),
    path("<slug:ingredient_slug>/", views.IngredientDetailsView.as_view(), name="ingredient-details"),
]