from django.contrib.auth.models import User
from django.db import models


class Seller(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zip = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    desc = models.CharField(max_length=500, blank=True, null=True)
    image = models.FileField(blank=True)
    image_content_type = models.CharField(max_length=50, blank=True)
    qrcode = models.FileField(blank=True)
    qrcode_content_type = models.CharField(max_length=50, blank=True)
