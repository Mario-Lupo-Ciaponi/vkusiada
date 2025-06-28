from django.db import models

from .choices import CategoryChoices

from ingredients.models import Ingredient
from accounts.models import VkusiadaUser
from common.mixins import SlugMixIn, AddedOnMixIn



class Recipe(SlugMixIn):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    category = models.CharField(
        max_length=100,
        choices=CategoryChoices
    )
    cuisine = models.CharField(
        max_length=100,
    )
    youtube_link = models.URLField(
        null=True,
        blank=True,
    )
    image_url = models.URLField()
    instructions = models.TextField()
    author = models.ForeignKey(
        "accounts.VkusiadaUser",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    users = models.ManyToManyField(
        "accounts.VkusiadaUser",
        related_name='saved_recipes',
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
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
        unique_together = ('recipe', 'ingredient')


class UserRecipe(AddedOnMixIn):
    user = models.ForeignKey(
        VkusiadaUser,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"

    class Meta:
        unique_together = ('user', 'recipe')


class Comment(AddedOnMixIn):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.CharField(
        max_length=50,
        default="Anonymous",
    )
    content = models.TextField()
