from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    amount = models.IntegerField()
    product_img = models.ImageField(upload_to='images/',default='images/default.jpeg')
