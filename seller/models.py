from django.contrib.auth.models import User
from django.db import models


class Seller(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    zip = models.DecimalField(max_digits=10, decimal_places=0, blank=True)
    desc = models.CharField(max_length=500, blank=True)
    image = models.FileField(blank=True)
    image_content_type = models.CharField(max_length=50, blank=True)
    qrcode = models.FileField(blank=True)
    qrcode_content_type = models.CharField(max_length=50, blank=True)

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
    status = models.SmallIntegerField(default=1, )
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
