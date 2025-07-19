from django.contrib.auth.models import AbstractUser
from django.db import models

from django_countries.fields import CountryField

from .choices import CookingLevelChoices


class VkusiadaUser(AbstractUser):
    ...


class Profile(models.Model):
    user = models.OneToOneField(
        VkusiadaUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )
    location = CountryField(
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    favourite_cuisine = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    cooking_level = models.CharField(
        max_length=50,
        choices=CookingLevelChoices,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username
