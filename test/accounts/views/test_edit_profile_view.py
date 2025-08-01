from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from accounts.choices import CookingLevelChoices


UserModel = get_user_model()


class TestEditProfileView(TestCase):
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

    def test__user_can_edit_their_own_profile(self):
        bio = "Test bio"
        cuisine = "Bulgarian"
        cooking_level = CookingLevelChoices.BEGINNER

        edit_data = {
            "bio": bio,
            "favourite_cuisine": cuisine,
            "cooking_level": cooking_level,
        }

        response = self.client.post(
            reverse("edit-profile", kwargs={"pk": self.user.pk}), data=edit_data
        )

        profile = Profile.objects.get(pk=self.user.pk)

        self.assertEqual(bio, profile.bio)
        self.assertEqual(cuisine, profile.favourite_cuisine)
        self.assertEqual(cooking_level, profile.cooking_level)

    def test__user_cannot_edit_others_profile(self):
        self.client.logout()

        user_credentials = {
            "username": "TestUse321321r2",
            "email": "test2@test.com",
            "password": "123tesdt1235",
        }

        user_2 = UserModel.objects.create_user(**user_credentials)

        self.client.login(
            username=user_credentials["username"],
            password=user_credentials["password"],
        )

        bio = "Test bio"
        cuisine = "Bulgarian"
        cooking_level = CookingLevelChoices.BEGINNER

        edit_data = {
            "bio": bio,
            "favourite_cuisine": cuisine,
            "cooking_level": cooking_level,
        }

        response = self.client.post(
            reverse("edit-profile", kwargs={"pk": self.user.pk}), data=edit_data
        )

        self.assertEqual(response.status_code, 403)

    def test__superuser_can_edit_any_profile(self):
        self.client.logout()

        superuser_credentials = {
            "username": "admin",
            "email": "admin2@admin.com",
            "password": "123admin1235",
        }

        superuser = UserModel.objects.create_superuser(**superuser_credentials)

        self.client.login(
            username=superuser_credentials["username"],
            password=superuser_credentials["password"],
        )

        bio = "Test bio superuser"
        cuisine = "Italian"
        cooking_level = CookingLevelChoices.ADVANCED

        edit_data = {
            "bio": bio,
            "favourite_cuisine": cuisine,
            "cooking_level": cooking_level,
        }

        response = self.client.post(
            reverse("edit-profile", kwargs={"pk": self.user.pk}), data=edit_data
        )

        profile = Profile.objects.get(pk=self.user.pk)

        self.assertEqual(bio, profile.bio)
        self.assertEqual(cuisine, profile.favourite_cuisine)
        self.assertEqual(cooking_level, profile.cooking_level)

    def test_that_successful_edit__redirects_to_the_account_details_view(self):
        response = self.client.post(
            reverse("edit-profile", kwargs={"pk": self.user.pk}), data={"bio": "test"}
        )

        self.assertRedirects(
            response, reverse("account-details", kwargs={"pk": self.user.pk})
        )
