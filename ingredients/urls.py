from django.urls import path, include
from ingredients import views


urlpatterns = [
    path("<slug:ingredient_slug>/", views.IngredientDetailsView.as_view(), name="ingredient_details"),
]