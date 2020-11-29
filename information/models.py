from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)

    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    birthday = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',bio="' + self.bio + '"'