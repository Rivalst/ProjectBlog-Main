from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


# ----- Start signals for user profile create -----
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     try:
#         instance.profile.save()
#     except Profile.DoesNotExist:
#         Profile.objects.create(user=instance)

# ----- End signals for user profile create-----
