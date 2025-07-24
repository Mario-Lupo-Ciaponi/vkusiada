from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from accounts.models import VkusiadaUser, Profile
from vkusiada.tasks import _send_mail


@receiver(post_save, sender=VkusiadaUser)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a VkusiadaUser is created.
    """

    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(m2m_changed, sender=Profile.followers.through)
def send_notification_to_followed_user(sender, instance, action, pk_set, **kwargs):
    """
    Signal to send a notification email to the user when they are followed by another user.
    This function is triggered when the followers field of a Profile instance is modified.
    """

    if action == "post_add":
        profile_owner = instance.user

        for follower_pk in pk_set:
            # Ensure that the follower exists before sending the email
            # this avoids potential errors if the follower has been deleted or does not exist.
            try:
                follower = VkusiadaUser.objects.get(pk=follower_pk)
                _send_mail.delay(
                    subject=f"{follower.username} started following you!",
                    message=f"Greeting {profile_owner.username}, \n\n{follower.username} started following "
                    f"your profile. Why don't you check out his/her profile and recipes?",
                    from_email=settings.DEFAULT_EMAIL,
                    recipient_list=[profile_owner.email],
                )
            except VkusiadaUser.DoesNotExist:
                continue
