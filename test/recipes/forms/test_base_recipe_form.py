from django.test import TestCase
from recipes.forms import BaseRecipeForm


class TestBaseForm(TestCase):
    def setUp(self):
        self.form = BaseRecipeForm()

    def test__name_placeholder_text(self):
        self.assertEqual(
            "Enter recipe name",
            self.form.Meta.widgets["name"].attrs["placeholder"],
        )

    def test__cuisine_placeholder_text(self):
        self.assertEqual(
            "Cuisine",
            self.form.Meta.widgets["cuisine"].attrs["placeholder"],
        )

    def test__youtube_link_placeholder_text(self):
        self.assertEqual(
            "YouTube link (optional)",
            self.form.Meta.widgets["youtube_link"].attrs["placeholder"],
        )

    def test__image_url_placeholder_text(self):
        self.assertEqual(
            "Image URL",
            self.form.Meta.widgets["image_url"].attrs["placeholder"],
        )

    def test__instructions_placeholder_text(self):
        self.assertEqual(
            "Instructions",
            self.form.Meta.widgets["instructions"].attrs["placeholder"],
        )

    def test__if_name_field_is_displayed(self):
        self.assertIn(
            "name",
            self.form.fields,
        )

    def test__if_cuisine_field_is_displayed(self):
        self.assertIn(
            "cuisine",
            self.form.fields,
        )

    def test__if_category_field_is_displayed(self):
        self.assertIn(
            "category",
            self.form.fields,
        )

    def test__if_youtube_link_is_displayed(self):
        self.assertIn(
            "youtube_link",
            self.form.fields,
        )

    def test__if_image_url_field_is_displayed(self):
        self.assertIn(
            "image_url",
            self.form.fields,
        )

    def test__if_instructions_field_is_displayed(self):
        self.assertIn(
            "instructions",
            self.form.fields,
        )

