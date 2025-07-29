from http.client import responses

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, UserRecipe


UserModel = get_user_model()


class TestRemoveSavedRecipe(TestCase):
    def setUp(self):
        self.user_credentials = {
            "username": "TestUser",
            "email": "test@test.com",
            "password": "123test1235",
        }

        self.user = UserModel.objects.create_user(**self.user_credentials)

        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

        self.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            category="Dessert",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            instructions="Random instructions",
            author=self.user,
        )

        UserRecipe.objects.create(
            recipe=self.test_recipe,
            user=self.user
        )

    def test__authenticated_users_can_remove_saved_recipes(self):
        self.client.post(
            reverse("remove-saved-recipe", kwargs={"recipe_slug": self.test_recipe.slug})
        )

        is_recipe_present = UserRecipe.objects.filter(recipe=self.test_recipe, user=self.user).exists()

        self.assertFalse(is_recipe_present)
    
    def test__when_recipe_is_removed__it_displays_appropriate_message(self):
        response = self.client.post(
            reverse("remove-saved-recipe", kwargs={"recipe_slug": self.test_recipe.slug})
        )

        message_expected = f"Recipe {self.test_recipe.name} was removed successfully"
        messages = list(get_messages(response.wsgi_request))

        self.assertIn(message_expected, [m.message for m in messages])

    def test__redirects_back_to_referer_page(self):
        response = self.client.post(
            reverse("remove-saved-recipe", kwargs={"recipe_slug": self.test_recipe.slug}),
            HTTP_REFERER=reverse("saved-recipes")
        )

        self.assertRedirects(response, reverse("saved-recipes"))
