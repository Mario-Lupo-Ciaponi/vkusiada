from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient


class TestIngredientDetailsView(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato")

        self.response = self.client.get(
            reverse(
                "ingredient-details", kwargs={"ingredient_slug": self.ingredient.slug}
            ),
        )

    def test__view_status_code__returns_200(self):
        status_code_expected = 200

        self.assertTrue(status_code_expected, self.response.status_code)

    def test__context_contains_correct_ingredient(self):
        self.assertEqual(self.response.context["ingredient"], self.ingredient)
