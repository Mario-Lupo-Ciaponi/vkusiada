from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, UserRecipe


UserModel = get_user_model()


class TestSaveRecipeView(TestCase):
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

    def test__authenticated_user_can_save_recipe(self):
        response = self.client.post(
            reverse("save-recipe", kwargs={"recipe_slug": self.test_recipe.slug}),
            # HTTP_REFERER=reverse("saved-ingredients")
        )

        is_recipe_saved = UserRecipe.objects.filter(
            recipe=self.test_recipe, user=self.user
        ).exists()

        self.assertTrue(is_recipe_saved)

    def test__user_is_redirected_back_to_the_referring_page(self):
        response = self.client.post(
            reverse("save-recipe", kwargs={"recipe_slug": self.test_recipe.slug}),
            HTTP_REFERER=reverse("search-recipe"),
        )

        self.assertRedirects(response, reverse("search-recipe"))

    def test__saving_same_recipe__raises_integrity_error(self):
        response = self.client.post(
            reverse("save-recipe", kwargs={"recipe_slug": self.test_recipe.slug}),
            HTTP_REFERER=reverse("search-recipe"),
        )

        response = self.client.post(
            reverse("save-recipe", kwargs={"recipe_slug": self.test_recipe.slug}),
            HTTP_REFERER=reverse("search-recipe"),
        )

        message_expected = f"You already saved the recipe!"

        messages = list(get_messages(response.wsgi_request))

        self.assertIn(message_expected, [m.message for m in messages])
