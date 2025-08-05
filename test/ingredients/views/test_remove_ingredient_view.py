from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient, UserIngredient

UserModel = get_user_model()


class TestRemoveIngredientView(TestCase):
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

        UserIngredient.objects.create(ingredient=self.ingredient_1, user=self.user)
        UserIngredient.objects.create(ingredient=self.ingredient_2, user=self.user)

    def test__removes_correct_ingredient_for_the_logged_in_user(self):
        self.assertTrue(
            UserIngredient.objects.filter(
                ingredient=self.ingredient_1, user=self.user
            ).exists()
        )

        response = self.client.post(
            reverse("remove-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk})
        )

        ingredient = Ingredient.objects.get(pk=self.ingredient_1.pk)
        is_ingredient_present = UserIngredient.objects.filter(
            ingredient=self.ingredient_1, user=self.user
        ).exists()

        message_expected = f"Ingredient {ingredient.name} was removed successfully"

        messages = list(get_messages(response.wsgi_request))

        self.assertFalse(is_ingredient_present)
        self.assertIn(message_expected, [m.message for m in messages])

    def test__if_redirects_to_saved_ingredients_page(self):
        response = self.client.post(
            reverse(
                "remove-ingredient", kwargs={"ingredient_pk": self.ingredient_1.pk}
            ),
            HTTP_REFERER=reverse("saved-ingredients"),
        )

        self.assertRedirects(response, reverse("saved-ingredients"))

    def test__when_trying_to_remove_a_ingredient_that_does_not_exist__returns_status_code_404(
        self,
    ):
        response = self.client.post(
            reverse("remove-ingredient", kwargs={"ingredient_pk": 999}),
        )

        self.assertEqual(response.status_code, 404)
