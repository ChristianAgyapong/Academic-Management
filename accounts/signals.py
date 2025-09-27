# Signals temporarily disabled to avoid conflicts with admin forms
# Profiles will be created manually through the admin interface or registration forms

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Profile, UserRole

# Uncomment and modify these signals when needed for programmatic user creation
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance, defaults={'role': UserRole.STUDENT})