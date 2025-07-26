from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from recipes.models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from common.choices import CategoryChoices


UserModel = get_user_model()


class TestRecipeModel(TestCase):
    def setUp(self):
        self.test_author = UserModel.objects.create_user(
            username="TestName",
            email="testtest@test.com",
            password="123test123",
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

        self.test_ingredient = Ingredient.objects.create(
            name="Test Ingredient",
        )

        self.test_recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.test_recipe, ingredient=self.test_ingredient, measure="2g"
        )

    def test__m2m_trough_relation__returns_true(self):
        self.assertIn(self.test_ingredient, self.test_recipe.ingredients.all())

    def test__model_str_method__returns_name(self):
        self.assertEqual(
            f"{self.test_recipe.name} - {self.test_ingredient.name}",
            str(self.test_recipe_ingredient),
        )

    def test__unique_constraint_of_recipe_and_ingredient_field__raises_integrity_error(
        self,
    ):
        with self.assertRaises(IntegrityError) as ie:
            RecipeIngredient.objects.create(
                recipe=self.test_recipe, ingredient=self.test_ingredient
            )

        self.assertIn("UNIQUE", str(ie.exception).upper())
