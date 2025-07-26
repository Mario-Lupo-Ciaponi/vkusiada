from django.test import TestCase
from recipes.forms import AddCommentForm


class TestAddCommentForm(TestCase):
    def setUp(self):
        self.form = AddCommentForm()

    def test__placeholder_text(self):
        self.assertEqual(
            "Add a comment...",
            self.form.Meta.widgets["content"].attrs["placeholder"],
        )
