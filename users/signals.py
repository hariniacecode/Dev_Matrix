from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    print("Profile Signal Triggered")

    if created:
        try:
            with transaction.atomic():

                # Create Profile
                profile = Profile.objects.create(
                    user=instance,
                    username=instance.username,
                    email=instance.email,
                    name=instance.first_name,
                )

                # Send welcome email
                send_mail(
                    subject="Welcome to DevSearch",
                    message="We are glad you are here!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[profile.email],
                    fail_silently=False
                )

        except Exception as e:
            print("Email failed:", e)

            # Delete the User if email failed
            instance.delete()


def updateUser(sender, instance, created, **kwargs):

    if not created:

        profile = instance
        user = profile.user

        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email

        user.save(
            update_fields=[
                "first_name",
                "username",
                "email"
            ]
        )


def deleteUser(sender, instance, **kwargs):

    try:
        user = instance.user
        user.delete()
    except Exception:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
  
