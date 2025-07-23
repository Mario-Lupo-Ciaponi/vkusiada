from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import Like
from vkusiada.tasks import _send_mail


@receiver(post_save, sender=Like)
def send_liked_recipe_email(sender, instance: Like, created, **kwargs):
    if created:
        _send_mail.delay(
            subject=f"{instance.user.username} liked your recipe.",
            message=f"Greetings {instance.recipe.author.username}, \n\n "
            f"{instance.user.username} liked your recipe '{instance.recipe.name}'!",
            from_email=settings.DEFAULT_EMAIL,
            recipient_list=[instance.recipe.author.email],
        )
