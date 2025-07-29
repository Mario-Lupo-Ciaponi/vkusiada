from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe
from common.models import Like


UserModel = get_user_model()


class TestLikeRecipeView(TestCase):
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

    def test__user_has_not_liked__like_the_recipe(self):
        response = self.client.get(
            reverse("like-recipe", kwargs={"recipe_slug": self.test_recipe.slug, "user_pk": self.user.pk})
        )

        did_user_like_recipe = Like.objects.filter(recipe=self.test_recipe, user=self.user).exists()

        self.assertTrue(did_user_like_recipe)

    def test__user_has_liked__unlike_the_recipe(self):
        Like.objects.create(
            recipe=self.test_recipe,
            user=self.user,
        )

        response = self.client.get(
            reverse("like-recipe", kwargs={"recipe_slug": self.test_recipe.slug, "user_pk": self.user.pk})
        )

        did_user_like_recipe = Like.objects.filter(recipe=self.test_recipe, user=self.user).exists()

        self.assertFalse(did_user_like_recipe)

    def test__like_redirects_back_to_referer(self):
        response = self.client.get(
            reverse("like-recipe", kwargs={"recipe_slug": self.test_recipe.slug, "user_pk": self.user.pk}),
            HTTP_REFERER=reverse("recipe_details", kwargs={"recipe_slug": self.test_recipe.slug})
        )

        self.assertRedirects(response, reverse("recipe_details", kwargs={"recipe_slug": self.test_recipe.slug}))
