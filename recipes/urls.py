from django.urls import path, include
from recipes import views
urlpatterns = [
    path("", views.SearchRecipeView.as_view(), name="search-recipe"),
    path("suggested-recipes/", views.SuggestedRecipesView.as_view(), name="suggested-recipes"),
    path("saved-recipes/", views.SavedRecipesView.as_view(), name="saved-recipes"),
    path("create/", views.CreateRecipeView.as_view(), name="create-recipe"),
    path("<slug:recipe_slug>/", include([
        path("details/", views.RecipeDetailView.as_view(), name="recipe_details"),
        path("edit/", views.EditRecipeView.as_view(), name="edit-recipe"),
        path("delete/", views.DeleteRecipeView.as_view(), name="delete-recipe"),
        path("remove-saved/", views.remove_saved_recipe, name="remove-saved-recipe"),
        path("save/", views.save_recipe, name="save-recipe"),
    ])),
    path("category/<str:category>/", views.FilteredCategoryView.as_view(), name="category_recipes"),
]