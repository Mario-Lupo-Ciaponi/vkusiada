from django.contrib.auth import get_user_model

from common.choices import CategoryChoices
from recipes.models import Recipe, Comment

from django.test import TestCase


UserModel = get_user_model()


class TestCommentModel(TestCase):
    def setUp(self):
        self.test_author = UserModel.objects.create_user(
            username="TestName",
            email="testtest@test.com",
            password="123test123",
        )

        self.test_user_to_comment = UserModel.objects.create_user(
            username="Test Second",
            email="ttest@test.com",
            password="123tedwast123",
        )

        self.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            category=CategoryChoices.DESSERT,
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Random instructions",
            author=self.test_author,
        )

        self.test_comment = Comment.objects.create(
            recipe=self.test_recipe,
            author=self.test_user_to_comment,
            content="A comment for test",
        )

    def test__related_name_of_recipe_works__returns_true(self):
        self.assertIn(self.test_comment, self.test_recipe.comments.all())

    def test__related_name_of_user_works__returns_true(self):
        self.assertIn(self.test_comment, self.test_user_to_comment.comments.all())

    def test__reverse_recipe_name__returns_recipe_object(self):
        self.assertEqual(self.test_comment.recipe, self.test_recipe)

    def test__reverse_user__returns_user_object(self):
        self.assertEqual(self.test_comment.recipe, self.test_recipe)
