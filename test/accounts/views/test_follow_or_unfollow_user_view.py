from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile

UserModel = get_user_model()


class TestFollowOrUnfollowUser(TestCase):
    def setUp(self):
        self.user_credentials_1 = {
            "username": "User1",
            "email": "test1@test.com",
            "password": "123test11235",
        }

        self.user_1 = UserModel.objects.create_user(**self.user_credentials_1)

        self.user_credentials_2 = {
            "username": "User2",
            "email": "test2@test.com",
            "password": "1233test11235",
        }

        self.user_2 = UserModel.objects.create_user(**self.user_credentials_2)

        self.client.login(
            username=self.user_credentials_1["username"],
            password=self.user_credentials_1["password"],
        )

        self.response = self.client.post(
            reverse("follow-user", kwargs={"pk": self.user_2.pk})
        )

    def test__user_can_follow_other_user(self):
        user_2_profile = Profile.objects.get(user=self.user_2)

        user_2_followers = [f for f in user_2_profile.followers.all()]

        message_expected = f"{self.user_2} followed successfully!"
        messages = list(get_messages(self.response.wsgi_request))

        self.assertIn(self.user_1, user_2_followers)
        self.assertIn(message_expected, [m.message for m in messages])

    def test__user_can_unfollow_another_user(self):
        response = self.client.post(
            reverse("follow-user", kwargs={"pk": self.user_2.pk})
        )

        user_2_profile = Profile.objects.get(user=self.user_2)

        user_2_followers = [f for f in user_2_profile.followers.all()]

        message_expected = f"{self.user_2} unfollowed successfully!"
        messages = list(get_messages(response.wsgi_request))

        self.assertNotIn(self.user_1, user_2_followers)
        self.assertIn(message_expected, [m.message for m in messages])

    def test__user_following_himself__raises_error(self):
        response = self.client.post(
            reverse("follow-user", kwargs={"pk": self.user_1.pk})
        )

        message_expected = "Cannot follow yourself!"
        messages = list(get_messages(response.wsgi_request))

        self.assertIn(message_expected, [m.message for m in messages])
