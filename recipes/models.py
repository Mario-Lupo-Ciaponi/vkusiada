from django.contrib.auth import get_user_model
from django.db import models

from common.choices import CategoryChoices

from ingredients.models import Ingredient
from accounts.models import VkusiadaUser
from common.mixins import SlugMixIn, AddedOnMixIn
from recipes.validations import IsYoutubeLinkValidValidator


User = get_user_model()


class Recipe(SlugMixIn, AddedOnMixIn):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    category = models.CharField(max_length=100, choices=CategoryChoices)
    cuisine = models.CharField(
        max_length=100,
    )
    youtube_link = models.URLField(
        null=True,
        blank=True,
        validators=[
            IsYoutubeLinkValidValidator(),
        ],
    )
    image_url = models.URLField()
    instructions = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    users = models.ManyToManyField(
        User,
        related_name="saved_recipes",
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-added_on", "name"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    measure = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"

    class Meta:
        unique_together = ("recipe", "ingredient")


class UserRecipe(AddedOnMixIn):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"

    class Meta:
        unique_together = ("user", "recipe")


class Comment(AddedOnMixIn):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
