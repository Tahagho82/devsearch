from .models import Profile
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete,pre_delete
from django.dispatch import receiver


# @receiver(post_save,sender = Profile)
def createProfile(sender, instance, created, **kwargs):
    print('Profile signal triggerd')
    if created:
        user1 = instance
        profile = Profile.objects.create(
            user=user1,
            username=user1.username,
            email=user1.email,
            name= user1.first_name
        )


def deleteUser(sender, instance, **kwargs):
    try : 
        user = instance.user
        user.delete()
    except:
        print('temp try')

post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)