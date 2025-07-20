from django.contrib.auth import get_user_model
from django.db import models

from common.mixins import SlugMixIn, AddedOnMixIn
from accounts.models import VkusiadaUser


User = get_user_model()


class Ingredient(SlugMixIn):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class UserIngredient(AddedOnMixIn):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"

    class Meta:
        unique_together = ('user', 'ingredient')
