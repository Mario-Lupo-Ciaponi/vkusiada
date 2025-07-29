from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, Comment


UserModel = get_user_model()


class TestDetailsViewComment(TestCase):
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

    def test__authenticated_user_can_post_comment(self):
        comment_content = "This is just a test comment."

        response = self.client.post(
            reverse("recipe_details",
                    kwargs={"recipe_slug": self.test_recipe.slug}
                    ),
                    data={"content": comment_content}
        )

        was_comment_posted = Comment.objects.filter(recipe=self.test_recipe, author=self.user).exists()

        self.assertTrue(was_comment_posted)

    def test__unauthenticated_user_can_post_comment__redirects_to_login_page(self):
        comment_content = "This is just a test comment."
        self.client.logout()

        response = self.client.post(
            reverse("recipe_details",
                    kwargs={"recipe_slug": self.test_recipe.slug}
                    ),
                    data={"content": comment_content}
        )

        self.assertRedirects(response, reverse("login"))
