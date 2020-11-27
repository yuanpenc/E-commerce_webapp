from django.contrib.auth.models import User
from django.db import models


class Items(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    stocks = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    detail = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='items')
    content_type = models.CharField(max_length=50, blank=True)
    status = models.SmallIntegerField(default=1,)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="item_creators")
    category = models.CharField(max_length=20)

class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comment_creators")
    content = models.CharField(max_length=500)
    creation_time = models.DateTimeField()
    belong_to = models.ForeignKey(Items, on_delete=models.PROTECT, related_name="item_comments")


