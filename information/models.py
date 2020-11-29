from django.contrib.auth.models import User
from django.db import models


# Create your models here.
<<<<<<< HEAD
=======
from django.db.models.signals import post_save
from django.dispatch import receiver

from goods.models import Items

>>>>>>> 764b33789c3e2709065332f7bf3668a288525dda

class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
<<<<<<< HEAD
    address = models.CharField(max_length=200)
    birthday = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'
=======
    address = models.CharField(max_length=200, default="Greenfield 829 Ave, Pittsburgh, PA")
    birthday = models.CharField(max_length=200, default="01-01-2020")
    gender = models.CharField(max_length=200, default="male")


    def __unicode__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cart",on_delete=models.CASCADE)
    goods = models.ForeignKey(Items,on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
>>>>>>> 764b33789c3e2709065332f7bf3668a288525dda
