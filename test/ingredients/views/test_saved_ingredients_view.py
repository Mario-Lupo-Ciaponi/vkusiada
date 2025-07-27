from django.contrib.auth import get_user_model
from django.test import TestCase

from ingredients.models import Ingredient


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

        self.ingredient_1 = Ingredient.objects.create(
            name="Tomato"
        )

        self.ingredient_2 = Ingredient.objects.create(
            name="Cheese"
        )

        self.ingredient_3 = Ingredient.objects.create(
            name="Cucumber"
        )