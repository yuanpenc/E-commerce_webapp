from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

from goods.models import Items
from information.models import Profile
from seller.models import Seller


class Order(models.Model):
    # customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    orderid = models.CharField(max_length=500)
    content = models.CharField(max_length=500, blank=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    comment = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=False)

