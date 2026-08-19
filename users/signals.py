from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    print("Profile Signal Triggered")

    if created:
        # Check if profile already exists
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                "username": instance.username,
                "email": instance.email,
                "name": instance.first_name,
            }
        )

        subject = "Welcome to DevSearch"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email

        # This saves the User, which triggers createProfile,
        # BUT createProfile sees created=False and does nothing.
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
  
