from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from Djangoadvanceproject.accounts.models import Profile, ThreeDUser
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()


@receiver(post_save, sender=ThreeDUser)
def create_profile_for_superuser(sender, instance, created, **kwargs):
    # Only create a profile if a superuser is created
    if created and instance.is_superuser:
        Profile.objects.get_or_create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
        print(f"Profile created for superuser {instance.email}")


@receiver(post_delete, sender=Profile)
def delete_user_on_profile_delete(sender, instance, **kwargs):
    # When a Profile is deleted, delete the associated user.
    user = instance.user
    if user:
        user.delete()