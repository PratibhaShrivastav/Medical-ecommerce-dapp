from django.db import models
from accounts.models import Cart
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    amount = models.IntegerField()
    price = models.IntegerField(default=100)
    product_img = models.ImageField(upload_to='images/',default='images/default.jpeg')
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
