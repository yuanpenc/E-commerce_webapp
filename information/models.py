from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver
from goods.models import Items


class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    address = models.CharField(max_length=200, default="No specific address")
    birthday = models.DateTimeField(default=datetime.now)
    gender = models.CharField(max_length=200, default="male")


    def __unicode__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart",on_delete=models.CASCADE)
    goods = models.ForeignKey(Items, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
