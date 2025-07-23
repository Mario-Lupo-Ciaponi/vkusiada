from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import Like
from recipes.models import Recipe
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


@receiver(post_save, sender=Recipe)
def send_followers_notification(sender, instance: Recipe, created, **kwargs):
    if created:
        author  = instance.author
        author_profile = author.profile
        author_followers = author_profile.followers.all()

        for follower in author_followers:
            _send_mail.delay(
                subject=f"{author.username} has created a new recipe!",
                message=f"{instance.name} has been created by {author.username} that you follow.",
                from_email=settings.DEFAULT_EMAIL,
                recipient_list=[follower.email],
            )

