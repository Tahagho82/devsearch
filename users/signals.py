from email import message
from .models import Profile
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings
# @receiver(post_save,sender = Profile)
def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggerd')
    if created:
        user1 = instance
        profile = Profile.objects.create(
            user=user1,
            username=user1.username,
            email=user1.email,
            name=user1.first_name
        )

        subject = 'Welcome to devsarch'
        message = 'We are glad you are here!'
# به خاطر محدودیت های گوگل نمیشه استفاده کرد
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created==False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        print('temp try')


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
