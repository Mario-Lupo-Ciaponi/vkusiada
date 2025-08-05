from django.test import TestCase

from ingredients.forms import IngredientBaseForm
from ingredients.models import Ingredient


class TestIngredientBaseForm(TestCase):
    def setUp(self):
        self.form_data = {"name": "tomato"}

    def test__form_with_valid_field_name__returns_true(self):
        form = IngredientBaseForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test__form_when_name_field_is_missing__returns_false(self):
        form_data = {}
        form = IngredientBaseForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test__when_name_field_is_a_duplicate__raises_custom_validation_error(self):
        unique_error_message = "Oh, no! Seems like this ingredient is already added!"
        Ingredient.objects.create(name="tomato")

        form = IngredientBaseForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(unique_error_message, form.errors.get("name")[0])
