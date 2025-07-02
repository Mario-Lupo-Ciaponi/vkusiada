from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import VkusiadaUser, Profile


@receiver(post_save, sender=VkusiadaUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
