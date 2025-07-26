from django.core.exceptions import ValidationError
from django.test import TestCase

from recipes.validations import IsYoutubeLinkValidValidator


class TestIsYoutubeLinkValidValidator(TestCase):
    def setUp(self):
        self.validator = IsYoutubeLinkValidValidator()

    def test__validator_with_valid_data(self):
        self.validator("https://www.youtube.com/watch?v=iVnU-vGt_xA")

    def test__validator_with_invalid_data__raises_validation_error(self):
        with self.assertRaises(ValidationError) as ve:
            self.validator("https://github.com/DiyanKalaydzhiev23/Django-Advanced/blob/"
                           "master/Testing/forumApp/test/posts/validators/test_bad_language_validator.py")

        self.assertTrue(str(ve))
