from django.urls import path, include
from recipes import views

urlpatterns = [
    path("", views.SearchRecipeView.as_view(), name="search-recipe"),
    path("saved-recipes/", views.SavedRecipesView.as_view(), name="saved-recipes"),
    path("create/", views.CreateRecipeView.as_view(), name="create-recipe"),
    path(
        "<slug:recipe_slug>/",
        include(
            [
                path(
                    "details/", views.RecipeDetailView.as_view(), name="recipe_details"
                ),
                path("edit/", views.EditRecipeView.as_view(), name="edit-recipe"),
                path("delete/", views.DeleteRecipeView.as_view(), name="delete-recipe"),
                path(
                    "remove-saved/",
                    views.remove_saved_recipe,
                    name="remove-saved-recipe",
                ),
                path("save/", views.save_recipe, name="save-recipe"),
                path("like/<int:user_pk>/", views.like_recipe, name="like-recipe"),
            ]
        ),
    ),
    path(
        "category/<str:category>/",
        views.FilteredCategoryView.as_view(),
        name="category_recipes",
    ),
    path(
        "comment/<int:pk>/",
        include(
            [
                path("edit/", views.EditCommentView.as_view(), name="edit-comment"),
                path(
                    "delete/", views.DeleteCommentView.as_view(), name="delete-comment"
                ),
            ]
        ),
    ),
    path(
        "user-<int:user_pk>/",
        views.RecipesCreatedByUserView.as_view(),
        name="recipes-created",
    ),
]
