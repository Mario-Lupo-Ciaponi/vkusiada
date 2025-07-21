from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe


UserModel = get_user_model()


class Like(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="likes_sent",
    )
