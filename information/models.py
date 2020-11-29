from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    address = models.CharField(max_length=200, default="Greenfield 829 Ave, Pittsburgh, PA")
    birthday = models.CharField(max_length=200, default="01-01-2020")
    gender = models.CharField(max_length=200, default="male")


    def __unicode__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'
