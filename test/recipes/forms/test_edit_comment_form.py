from django.test import TestCase
from recipes.forms import EditCommentForm


class TestEditCommentForm(TestCase):
    def setUp(self):
        self.form = EditCommentForm()

    def test__if_comment_is_added(self):
        self.assertEqual(
            "Edit the comment",
            self.form.Meta.widgets["content"].attrs["placeholder"],
        )
