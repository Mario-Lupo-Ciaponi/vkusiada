from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, RecipeIngredient, UserRecipe
from ingredients.models import Ingredient, UserIngredient


UserModel = get_user_model()



class TestIndexView(TestCase):
    def setUp(self):
        self.user_credentials= {
            "username": "TestUser",
            "email": "test@test.com",
            "password": "123test1235",
        }

        self.user = UserModel.objects.create_user(**self.user_credentials)

        self.test_recipe = Recipe.objects.create(
            name="Test Recipe",
            category="Dessert",
            cuisine="Bu",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        self.test_ingredient = Ingredient.objects.create(
            name="Test Ingredient"
        )

        self.test_recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.test_recipe,
            ingredient=self.test_ingredient,
            measure="2g",
        )

        self.user_ingredient = UserIngredient.objects.create(
            user=self.user,
            ingredient=self.test_ingredient,
        )

        self.client.login(
            username=self.user_credentials["username"],
            password=self.user_credentials["password"]
        )

    def test__rendered_template_if_user_not_authenticated__should_display_appropriate_message(self):
        self.client.logout()
        response = self.client.get(reverse("index"))

        self.assertContains(response, "Hey! If you want suggestions based on your ingredients, you need to")

    def test__rendered_template_if_user_is_authenticated_but_does_not_have_ingredients__should_display_appropriate_message(self):
        UserIngredient.objects.all().delete()

        response = self.client.get(reverse("index"))

        self.assertContains(response, "No recipe suggestions...")

    def test__rendered_template_if_user_is_authenticated_and_has_ingredients__should_display_appropriate_message(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "Test Recipe")

    def test__rendered_template_if_user_is_authenticated_and_has_a_recipe_saved__should_display_only_one_recipe(self):
        recipe_test_2 = Recipe.objects.create(
            name="Test Recipe 2",
            category="Dessert",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_2,
            ingredient=self.test_ingredient
        )

        UserRecipe.objects.create(
            recipe=self.test_recipe,
            user=self.user
        )

        response = self.client.get(reverse("index"))

        self.assertContains(response, "Test Recipe 2")

    def test__query_filtering__should_display_filtered_recipes(self):
        recipe_test_2 = Recipe.objects.create(
            name="Chicken",
            category="Entrees",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_2,
            ingredient=self.test_ingredient
        )

        response = self.client.get(reverse("index"), {"query": "chiCken"})

        self.assertContains(response, "Chicken")
        self.assertNotContains(response, "Test Recipe")

    def test__category_filtering__should_display_filtered_recipes(self):
        recipe_test_2 = Recipe.objects.create(
            name="Chicken",
            category="Entrees",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_2,
            ingredient=self.test_ingredient
        )

        response = self.client.get(reverse("index"), {"category": "Entrees"})

        self.assertContains(response, "Chicken")
        self.assertNotContains(response, "Test Recipe")

    def test__category_filtering_with_all__should_display_filtered_recipes(self):
        recipe_test_2 = Recipe.objects.create(
            name="Chicken",
            category="Entrees",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_2,
            ingredient=self.test_ingredient
        )

        response = self.client.get(reverse("index"), {"category": "All"})

        self.assertContains(response, "Chicken")
        self.assertContains(response, "Test Recipe")

    def test__category_and_query_filtering__should_display_filtered_recipes(self):
        recipe_test_2 = Recipe.objects.create(
            name="Pizza",
            category="Entrees",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_2,
            ingredient=self.test_ingredient
        )

        recipe_test_3 = Recipe.objects.create(
            name="Pasta",
            category="Entrees",
            cuisine="Italian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )

        RecipeIngredient.objects.create(
            recipe=recipe_test_3,
            ingredient=self.test_ingredient
        )

        response = self.client.get(reverse("index"), {"category": "Entrees", "query": "paSTa"})

        self.assertContains(response, "Pasta")
        self.assertNotContains(response, "Pizza")
        self.assertNotContains(response, "Test Recipe")

    def test__user_has_ingredients_but_no_recipes_use_them__should_display_appropriate_message(self):
        UserIngredient.objects.all().delete()

        test_ingredient_2 = Ingredient.objects.create(
            name="Second test ingredient"
        )

        UserIngredient.objects.create(
            user=self.user,
            ingredient=test_ingredient_2
        )

        response = self.client.get(reverse("index"))

        self.assertContains(response, "No recipe suggestions...")

    def test__recipe_has_no_ingredient__should_not_show_up(self):
        test_recipe_3 = Recipe.objects.create(
            name="Test Recipe 3",
            category="Dessert",
            cuisine="Bulgarian",
            youtube_link="https://www.youtube.com/watch?v=iVnU-vGt_xA",
            image_url="https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",
            instructions="Just for test",
            author=self.user,
        )
        response = self.client.get(reverse("index"))

        self.assertNotContains(response, "Test Recipe 3")

    def test__if_search_form_and_current_page_are_present_in_the_contex(self):
        response = self.client.get(reverse("index"))

        self.assertIn("search_form", response.context)
        self.assertIn("current_page", response.context)

    def test__if_current_page_is_equal_to_index(self):
        response = self.client.get(reverse("index"))

        self.assertEqual("index", response.context["current_page"])

