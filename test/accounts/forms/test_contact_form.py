from django.test import TestCase

from accounts.forms import ContactForm


class TestContactForm(TestCase):
    def setUp(self):
        self.form_data = {
            "email": "mario.lupo.ciaponi08@gmail.com",
            "subject": "Test Subject",
            "content": "This is just a test content to see if everything is alright!",
        }

    def test__if_form_passes_with_valid_data__returns_true(self):
        form = ContactForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test__if_form_passes_with_missing_data__returns_false(self):
        form_data = {
            "email": "mario.lupo.ciaponi08@gmail.com",
            "content": "This is just a test content to see if everything is alright!",
        }

        form = ContactForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test__if_content_is_too_short(self):
        self.form_data["content"] = "Test"

        form = ContactForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test__if_labels_are_empty(self):
        field_has_label = []

        for field in ContactForm.base_fields:
            if ContactForm.base_fields[field].label is None:
                field_has_label.append(False)
            else:
                field_has_label.append(True)

        self.assertNotIn(True, field_has_label)
