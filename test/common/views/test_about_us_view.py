from django.test import TestCase
from django.urls import reverse


class TestAboutUsView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("about-us"))

    def test__if_the_right_template_is_rendered(self):
        template_name = "common/about-us.html"

        self.assertTemplateUsed(self.response, template_name)

    def test__if_the_current_page_is_about_us(self):
        expected_template_name = "about_us"

        self.assertEqual(self.response.context["current_page"], expected_template_name)
