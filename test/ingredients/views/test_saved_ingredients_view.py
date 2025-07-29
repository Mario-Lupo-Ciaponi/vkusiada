from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient, UserIngredient


UserModel = get_user_model()


class TestSavedIngredientsView(TestCase):
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

        UserIngredient.objects.create(user=self.user, ingredient=self.ingredient_3)

        UserIngredient.objects.create(user=self.user, ingredient=self.ingredient_1)

    def test__only_shows_ingredients_saved_by_logged_in_user(self):
        response = self.client.get(reverse("saved-ingredients"))

        ingredients_expected = list(
            Ingredient.objects.exclude(name=self.ingredient_2.name).order_by("name")
        )
        context_ingredients = [i.ingredient for i in response.context["ingredients"]]

        self.assertEqual(ingredients_expected, context_ingredients)

    def test__filters_results_by_query_param(self):
        response = self.client.get(reverse("saved-ingredients"), {"query": "toMA"})

        ingredients_expected = list(
            Ingredient.objects.exclude(
                Q(name=self.ingredient_2.name) | Q(name=self.ingredient_3.name)
            ).order_by("name")
        )
        context_ingredients = [i.ingredient for i in response.context["ingredients"]]

        self.assertEqual(ingredients_expected, context_ingredients)

    def test__pagination_works_when_there_are_more_than_7_ingredients(self):
        ingredient_4 = Ingredient.objects.create(name="Avocado")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_4)

        ingredient_5 = Ingredient.objects.create(name="Lettuce")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_5)

        ingredient_6 = Ingredient.objects.create(name="Pickles")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_6)

        ingredient_7 = Ingredient.objects.create(name="Chicken")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_7)

        ingredient_8 = Ingredient.objects.create(name="Sugar")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_8)

        ingredient_9 = Ingredient.objects.create(name="Salt")
        UserIngredient.objects.create(user=self.user, ingredient=ingredient_9)

        response = self.client.get(reverse("saved-ingredients"))

        expected_ingredients = list(
            UserIngredient.objects.filter(user=self.user).order_by("ingredient__name")[
                :7
            ]
        )
        context_ingredients = list(response.context["ingredients"])

        self.assertEqual(context_ingredients, expected_ingredients)

    def test__view_redirects_if_user_not_logged_in(self):
        self.client.logout()

        response = self.client.get(reverse("saved-ingredients"), follow=False)

        expected_login_url = f"{reverse("login")}?next={reverse("saved-ingredients")}"

        self.assertRedirects(response, expected_login_url)
