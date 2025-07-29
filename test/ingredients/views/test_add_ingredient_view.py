from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient, UserIngredient


UserModel = get_user_model()


class TestAddIngredientView(TestCase):
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

    def test__unauthenticated_user_sees_all_ingredients(self):
        self.client.logout()

        response = self.client.get(reverse("add-ingredient"))

        context_ingredients = list(response.context["ingredient_list"])
        all_ingredients = list(Ingredient.objects.all().order_by("name"))

        self.assertEqual(context_ingredients, all_ingredients)

    def test__filter_functionality_works__returns_filtered_ingredients(self):
        response = self.client.get(reverse("add-ingredient"), {"query": "cHEesE"})

        self.assertContains(response, "Cheese")

    def test__authenticated_user_sees_only_ingredients_they_have_not_added(self):
        UserIngredient.objects.create(user=self.user, ingredient=self.ingredient_2)

        response = self.client.get(reverse("add-ingredient"))

        ingredients_expected = list(
            Ingredient.objects.exclude(name=self.ingredient_2.name).order_by("name")
        )
        context_ingredients = list(response.context["ingredient_list"])

        self.assertEqual(ingredients_expected, context_ingredients)

    def test__search_exclusion_both_work_together(self):
        UserIngredient.objects.create(
            user=self.user,
            ingredient=self.ingredient_3,
        )

        response = self.client.get(reverse("add-ingredient"), {"query": "c"})

        ingredients_expected = list(
            Ingredient.objects.exclude(
                Q(name=self.ingredient_1.name) | Q(name=self.ingredient_3.name)
            )
        )
        context_ingredients = list(response.context["ingredient_list"])

        self.assertEqual(ingredients_expected, context_ingredients)
