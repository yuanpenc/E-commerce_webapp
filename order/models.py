from django.db import models

# Create your models here.
from goods.models import Items
from seller.models import Seller


class Order(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    comment = models.CharField(max_length=100, blank=True)