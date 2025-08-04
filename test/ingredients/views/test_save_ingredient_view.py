from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient, UserIngredient

UserModel = get_user_model()


class TestSaveIngredient(TestCase):
    def setUp(self):
        self.user_credentials = {
            "username": "TestUser",
            "email": "test@test.com",
            "password": "123test1235",
        }

        self.user = UserModel.objects.create_user(**self.user_credentials)

        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"],
        )

        self.ingredient_1 = Ingredient.objects.create(name="Tomato")

        self.ingredient_2 = Ingredient.objects.create(name="Cheese")

        self.ingredient_3 = Ingredient.objects.create(name="Cucumber")

    def test__adds_to_user_ingredients_if_user_has_not_already_saved_it(self):
        response = self.client.post(
            reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})
        )

        user_ingredient = UserIngredient.objects.filter(
            user=self.user, ingredient=self.ingredient_1
        ).exists()

        self.assertTrue(user_ingredient)

    def test__if_redirects_to_add_ingredient_on_success(self):
        response = self.client.post(
            reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})
        )

        self.assertRedirects(response, reverse("browse-ingredients"))

    def test__view_redirects_to_login_if_user_is_not_login(self):
        self.client.logout()
        response = self.client.post(
            reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})
        )

        expected_login_url = f"{reverse("login")}?next={reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})}"

        self.assertRedirects(response, expected_login_url)

    def test_does_not_add_duplicate_if_already_saved(self):
        response = self.client.post(
            reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})
        )
        response = self.client.post(
            reverse("save-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk}),
            follow=True,
        )

        ingredient = self.ingredient_1

        message_expected = f"{ingredient.name} already added!"

        messages = list(get_messages(response.wsgi_request))

        self.assertIn(message_expected, [m.message for m in messages])
