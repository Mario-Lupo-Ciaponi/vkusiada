from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from recipes.models import Recipe
from common.choices import CategoryChoices


UserModel = get_user_model()


class TestRecipeModel(TestCase):
    def setUp(self):
        self.test_author = UserModel.objects.create_user(
            username="TestName",
            email="testtest@test.com",
            password="123test123",
        )

        self.name = "Test Recipe"
        self.category = CategoryChoices.DESSERT
        self.cuisine = "Bulgarian"
        self.youtube_link = "https://www.youtube.com/watch?v=iVnU-vGt_xA"
        self.image_url = "https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D"
        self.instructions = "Random instructions"

        self.test_recipe = Recipe.objects.create(
            name=self.name,
            category=self.category,
            cuisine=self.cuisine,
            youtube_link=self.youtube_link,
            image_url=self.youtube_link,
            instructions=self.instructions,
            author=self.test_author,
        )

    def test__model_str_method__returns_name(self):
        self.assertEqual(self.name, str(self.test_recipe))

    def test__unique_constraint_of_name_field__raises_integrity_error(self):
        with self.assertRaises(IntegrityError) as ie:
            Recipe.objects.create(
                name=self.name,
                category=self.category,
                cuisine=self.cuisine,
                youtube_link=self.youtube_link,
                image_url=self.youtube_link,
                instructions=self.instructions,
                author=self.test_author,
            )

        self.assertIn("UNIQUE", str(ie.exception).upper())

    def test__invalid_category_choices__raises_validation_error(self):
        recipe_3 = Recipe(
            name="Random name",
            category="Invalid Category",
            cuisine=self.cuisine,
            youtube_link=self.youtube_link,
            image_url=self.youtube_link,
            instructions=self.instructions,
            author=self.test_author,
        )

        with self.assertRaises(ValidationError) as ve:
            recipe_3.full_clean()

        self.assertIn("not a valid choice", dict(ve.exception)["category"][0])

    def test__slug_mixin_auto_generates_a_slug_from_name(self):
        self.assertEqual("test-recipe", self.test_recipe.slug)
