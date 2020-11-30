from django.contrib.auth.models import User
from django.db import models

from seller.models import Seller


class Items(models.Model):
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    stocks = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    detail = models.CharField(max_length=4000)
    image = models.ImageField(upload_to='items', blank=True)
    content_type = models.CharField(max_length=50, blank=True)
    status = models.SmallIntegerField(default=1, )
    created_by = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)


class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comment_creators")
    content = models.CharField(max_length=500)
    creation_time = models.DateTimeField()
    belong_to = models.ForeignKey(Items, on_delete=models.PROTECT, related_name="item_comments")
